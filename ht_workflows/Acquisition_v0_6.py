#!/usr/bin/env python
# coding: utf-8

# In[78]:


import os
import win32com.client
import numpy as np
import time
import h5py
import sidpy
import pyNSID
import progressbar
import matplotlib.pyplot as plt
from IPython.display import clear_output

class Acquisition():
    def __init__(self, exe_path = "G:\My Drive\AE\PyAE\BEPyAE 022823 01\BEPyAE.exe", client = "BEPyAE.Application", 
                 pyae_vi = "\BE_PyAE_01.vi", pyscanner_vi = "\FPGA PyScanner\FPGA_PyScanner_01.vi") -> None:      
        # Start BEPyAE
        os.startfile(exe_path)

        # Wait BEPyAe to start, then get vi reference 'BEPyAE.vi' from BEPyAE directory
        bepyae_not_start = True
        while bepyae_not_start:
            try:
                self.labview = win32com.client.Dispatch(client)
                self.VI = self.labview.getvireference(exe_path + pyae_vi)
                bepyae_not_start = False
            except:
                time.sleep(1)
        # Get pyscanner vi
        if pyscanner_vi != None:
            self.VIs = self.labview.getvireference(exe_path + pyscanner_vi) 

    #initialize_labview
    def init_BEPyAE(self, offline_development = False):
        # Set measurement
        self.VI.setcontrolvalue('offline_development_control_cluster', 
                           (offline_development,offline_development,offline_development,offline_development))
        
        # Initialize Igor 
        self.VI.setcontrolvalue('initialize_AR18_control_cluster', (True,))
        # Wait until initializing is done
        while self.VI.getcontrolvalue('initialize_AR18_control_cluster')[0]:
            time.sleep(0.2)
        # igor_para = self.VI.getcontrolvalue('main tab') 
        self.AR_paras = self.VI.getcontrolvalue('initialize_AR18_indicator_cluster')
        
        return
    
    # Helf functions
    def progress_bar(self, max_value):
        widgets = [' [',
                   progressbar.Timer(format= 'progress: %(elapsed)s'),
                   '] ', progressbar.Bar('*'),' (',progressbar.ETA(), ') ',]
        bar = progressbar.ProgressBar(max_value=max_value, widgets=widgets).start()
        return bar

    def mk_dset(self, file_name, pfm_imgstack, channel_imgstack, complex_spectra,
                start_x, finish_x, start_y, finish_y, coordinates = None, beps = False, fit = False):
        '''
        Make hdf5 file to save all data
        igor scan size: image size in igorpro; start x, y and finish x, y: start and finish points
        
        '''
        # scan parameters
        # scan_size_x = self.AR_paras[1][1]
        # scan_size_y = self.AR_paras[1][2]
        scan_size_x = 10e-6
        scan_size_y = 10e-6
        len_x = np.abs(finish_x - start_x)
        len_y = np.abs(finish_y - start_y)

        # Fast fit pfm images
        dset_imgs = sidpy.Dataset.from_array(pfm_imgstack, title = 'be stack')
        dset_imgs.data_type = 'image_stack'
        dset_imgs.quantity = 'quick fit pfm'

        dset_imgs.set_dimension(0, sidpy.Dimension(np.linspace(0, 1, dset_imgs.shape[0])*(scan_size_y*len_y)/2,
                                name = "y axis", units = "m", quantity = "y axis", dimension_type = "spatial"))
        dset_imgs.set_dimension(1, sidpy.Dimension(np.linspace(0, 1, dset_imgs.shape[1])*(scan_size_x*len_x)/2,
                                name = "x axis", units = "m", quantity = "x axis", dimension_type = "spatial"))
        dset_imgs.set_dimension(2, sidpy.Dimension(np.arange(dset_imgs.shape[2]), 
                                name = "BE responses", quantity = "channels", dimension_type = "frame"))
        
        # channel images
        dset_chns = sidpy.Dataset.from_array(channel_imgstack, title = 'channel stack')
        dset_chns.data_type = 'image_stack'
        dset_chns.quantity = 'channels'

        dset_chns.set_dimension(0, sidpy.Dimension(np.linspace(0, 1, dset_chns.shape[0])*(scan_size_y*len_y)/2,
                                name = "y axis", units = "m", quantity = "y axis", dimension_type = "spatial"))
        dset_chns.set_dimension(1, sidpy.Dimension(np.linspace(0, 1, dset_chns.shape[1])*(scan_size_x*len_x)/2,
                                name = "x axis", units = "m", quantity = "x axis", dimension_type = "spatial"))
        dset_chns.set_dimension(2, sidpy.Dimension(np.arange(dset_chns.shape[2]), 
                                name = "channels images", quantity = "channels", dimension_type = "frame"))

        # Complex spectra
        complex_spectra_arr = np.asarray(complex_spectra)
        # complex_spectra_arr = complex_spectra_arr.reshape((imgstack.shape[0], imgstack.shape[1], -1, 2))

        dset_complex_spectra = sidpy.Dataset.from_array(complex_spectra_arr[...,0] + 1j*complex_spectra_arr[...,1], title = 'complex_spectra')
        dset_complex_spectra.quantity = 'pfm complex spectra'
        dset_complex_spectra.units = 'V'

        dset_complex_spectra.set_dimension(0, sidpy.Dimension(np.arange(pfm_imgstack.shape[0])*(pfm_imgstack.shape[1]),
                                            name = 'location index y', quantity = 'index ', dimension_type = 'spatial'))

        dset_complex_spectra.set_dimension(1, sidpy.Dimension(np.arange(dset_complex_spectra.shape[1]),
                                            name = 'location index x', units = 'Hz',quantity = 'index',dimension_type = 'spatial'))

        # create hdf5 file to save data
        suf = 0
        save_name = "{}_{}.hf5".format(file_name, suf)
        # update suffex if file already exists
        while os.path.exists(save_name):
            suf += 1
            save_name = "{}_{}.hf5".format(file_name, suf)

        hf = h5py.File(save_name, 'a')

        # save BE pulse parameters
        beparms = self.VI.getcontrolvalue('BE_pulse_control_cluster')
        hf['BE Parameters/pulse parameters'] = np.asarray(beparms)

        # frequency spectral
        fft_fres = np.asarray(self.VI.getcontrolvalue('BE_pulse_parm_indicator_cluster')[6])
        fft_bin_idx = np.asarray(self.VI.getcontrolvalue('BE_pulse_parm_indicator_cluster')[3])
        fre_arr = fft_fres[fft_bin_idx]
        hf['BE Parameters/frequency'] = np.asarray(fre_arr)

        # image size
        img_size = np.asarray([(dset_imgs.shape[0])*(scan_size_y*len_y)/2, (dset_imgs.shape[1])*(scan_size_x*len_x)/2])
        hf['BE Parameters/scan size'] = img_size

        # for BEPS data, we save DC waveform as well
        if beps == True:
            vec_dc = self.VI.getcontrolvalue("BEPS_VS_indicator_cluster")[0]
            vec_dc = np.asarray(vec_dc)
            hf['BEPS/vdc_waveform'] = vec_dc
            hf['BEPS/coordinates'] = coordinates

        # save quick fitting images
        hf.create_group("BE Quick Fitting") 
        pyNSID.hdf_io.write_nsid_dataset(dset_imgs, hf['BE Quick Fitting'], main_data_name="Quick Fitting")

        # save channel images
        hf.create_group("BE Channels") 
        pyNSID.hdf_io.write_nsid_dataset(dset_chns, hf['BE Channels'], main_data_name="Channels")
        
        # save complex spectral
        hf.create_group("BE Complex Spectra") 
        pyNSID.hdf_io.write_nsid_dataset(dset_complex_spectra, hf['BE Complex Spectra'], main_data_name="Complex Spectra")

        hf.close()

        if beps == False:
            return dset_imgs, dset_chns, dset_complex_spectra
        elif beps == True:
            return vec_dc, dset_imgs, dset_chns, dset_complex_spectra
        
    # define a function to convert coordinates to the parameters of microscopy probe location 
    def convert_coordinates(original_coordinates, start_x = -1, finish_x = 1, start_y = -1, finish_y = 1):
        original_coordinates = np.asarray(original_coordinates, dtype = np.float64()) # convert to int to float first
        coor_x = original_coordinates [1]
        coor_y = original_coordinates [0]
        # rescale the data to be symmetric around 0
        convert_x = (coor_x - (coor_x.max() - coor_x.min())/2) / (coor_x.max() - coor_x.min())
        convert_y = (coor_y - (coor_y.max() - coor_y.min())/2) / (coor_y.max() - coor_y.min())
    
        # shift and scale it to the scan range
        convert_x = convert_x * (finish_x - start_x) + (finish_x + start_x) / 2
        convert_y = convert_y * (finish_y - start_y) + (finish_y + start_y) / 2
    
        converted_locations = np.copy(original_coordinates)
        converted_locations[1] = convert_x
        converted_locations[0] = convert_y
    
        return converted_locations

    def tip_control(self, tip_parms_dict=None, do_move_tip = True, do_set_setpoint = True, feedbackon = True):
        """
        tip_parms_dict: Dictionary of tip control parameters. 
        Notes: range of next_x_pos_00 and next_y_pos_00 is from -1 to 1
        e.g., tip_parms_dict = {"set_point_V_00": 1}; set_setpoint = True; move_tip = True
        Default parameters are the values shown on the panel now.
        """ 
        # read current parameters
        default_setpoint_cluster = self.VI.getcontrolvalue('set_setpoint_control_cluster')  # get setpoint value
        default_move_tip_cluster = self.VI.getcontrolvalue('move_tip_control_cluster')  # get tip control parameters

        # Set default values for tip control parameters
        tip_parms_list = [default_setpoint_cluster[0], default_move_tip_cluster[0], default_move_tip_cluster[1], default_move_tip_cluster[2]]
        
        tip_parms_name_list = ["set_point_V_00", "next_x_pos_00", "next_y_pos_01", "transit_time_s_02"]
        
        # if user customized some parameters, set the parameters as customized values
        if tip_parms_dict != None:
            for i in range (len (tip_parms_list)):
                if tip_parms_name_list[i] in tip_parms_dict:
                    tip_parms_list[i] = tip_parms_dict[tip_parms_name_list[i]]
        
        # Set tip parameters. Here each variable was set above. 
        # if we set 'do_set_setpoint_01' and 'do_move_tip_03' to "False", 
        # # we will only input above parameters into PyAE but do not perform the actions
        self.VI.setcontrolvalue('set_setpoint_control_cluster', 
                                (tip_parms_list[0], do_set_setpoint))
        # wait until set setpoint is done
        while self.VI.getcontrolvalue("set_setpoint_control_cluster")[1]:
            time.sleep(0.1)

        self.VI.setcontrolvalue('move_tip_control_cluster', 
                                (tip_parms_list[1], 
                                 tip_parms_list[2], 
                                 tip_parms_list[3],
                                 do_move_tip))
        
        # while tip is moving, wait until tip move is done
        while self.VI.getcontrolvalue('move_tip_control_cluster')[3]:
            time.sleep(0.1)  # Wait 0.1 s and check if action is done again

        # return parameters
        if feedbackon == True:
            # return setpoint
            setpoint_parms = self.VI.getcontrolvalue('set_setpoint_control_cluster')
            print("Setpoint is: ", setpoint_parms[0])
            # return move tip parameter
            move_tip_parms = self.VI.getcontrolvalue('move_tip_control_cluster')
            print("Tip parameters are: ", move_tip_parms[:-1])
            
            print("Please reset if some parameters are incorrect")

        return

    def define_io_cluster (self, IO_cluster_parms_dict = None, do_set_IO = True):
        """
        IO_cluster_parms_dict: Dictionary of IO cluster parameters.
        e.g., IO_cluster_parms_dict = {"alog_output_amplifier_06": 10, "channel_01_type_07": 1}; 
        Default parameters are the ones showing in the IO_Control_cluster panel now
        """
        # Get default values for IO
        default_io_cluster = self.VI.getcontrolvalue('IO_control_cluster')

        IO_cluster_parms_list = [default_io_cluster[0], default_io_cluster[1], default_io_cluster[2],
                                 default_io_cluster[3], default_io_cluster[4], default_io_cluster[5],
                                 default_io_cluster[6], default_io_cluster[7], default_io_cluster[8],
                                 default_io_cluster[9], default_io_cluster[10]]
        IO_cluster_parms_name_list = ["AFM_platform_00", "DAQ_card_01", "IO_rate_02", 
                                      "analog_input_range_03", "analog_output_range_04",
                                      "analog_output_routing_05", "analog_output_amplifier_06", 
                                      "channel_01_type_07", "channel_02_type_08", 
                                      "channel_03_type_09", "IO_trigger_ring_10"]
        
        # if user customized some parameters, set the parameters as customized values
        if IO_cluster_parms_dict != None:
            for i in range (len (IO_cluster_parms_list)):
                if IO_cluster_parms_name_list[i] in IO_cluster_parms_dict:
                    IO_cluster_parms_list[i] = IO_cluster_parms_dict[IO_cluster_parms_name_list[i]]

        # Set IO cluster 
        # self.VI.setcontrolvalue('IO_control_cluster', 
        #                         (IO_cluster_parms_list[0], IO_cluster_parms_list[1], 
        #                          float(IO_cluster_parms_list[2]), float(IO_cluster_parms_list[3]), 
        #                          float(IO_cluster_parms_list[4]), float(IO_cluster_parms_list[5]), 
        #                          float(IO_cluster_parms_list[6]), IO_cluster_parms_list[7],
        #                          IO_cluster_parms_list[8], IO_cluster_parms_list[9], 
        #                          IO_cluster_parms_list[10], do_set_IO))
        
        self.VI.setcontrolvalue('IO_control_cluster', 
                                (IO_cluster_parms_list[0], IO_cluster_parms_list[1], 
                                 IO_cluster_parms_list[2], IO_cluster_parms_list[3], 
                                 IO_cluster_parms_list[4], IO_cluster_parms_list[5], 
                                 IO_cluster_parms_list[6], IO_cluster_parms_list[7],
                                 IO_cluster_parms_list[8], IO_cluster_parms_list[9], 
                                 IO_cluster_parms_list[10], do_set_IO))
        
        # Get BE pulse cluster. We can get (and save) BE pulse parameters for post measurement analysis
        IO_parms = self.VI.getcontrolvalue('IO_indicator_cluster')
        print("IO control parameters are: ", IO_parms)
        print("Please reset if some parameters are incorrect")
        return 
    
    def define_be_parms(self, be_parms_dict=None, do_create_be_waveform = True, feedbackon = True):
        """
        be_parms_dict: Dictionary of BE parameters. 
        e.g., be_parms_dict = {"center_frequency_Hz_00": 350, "band_width_Hz_01": 100000}
        Default parameters are the values shown in the panel now
        """ 
        # Get default values for BE parameters
        default_be_cluster = self.VI.getcontrolvalue('BE_pulse_control_cluster')
        
        # Set default values for BE parameters
        be_parms_list = [default_be_cluster[0]/1000, default_be_cluster[1]/1000, default_be_cluster[2],
                         default_be_cluster[3], default_be_cluster[4], default_be_cluster[5]*1000,
                         default_be_cluster[6], default_be_cluster[7]/1000, default_be_cluster[8]*1000]
        be_parms_name_list = ["center_frequency_Hz_00", "band_width_Hz_01", "amplitude_V_02", 
                              "phase_variation_03", "repeats_04", "req_pulse_duration_s_05",
                              "auto_smooth_ring_06", "edge_smoothing_Hz_07", "window_adjustment_08"]
        
        # if user customized some parameters, set the parameters as customized values
        if be_parms_dict != None:
            for i in range (len (be_parms_list)):
                if be_parms_name_list[i] in be_parms_dict:
                    be_parms_list[i] = be_parms_dict[be_parms_name_list[i]]
 
        # Set BE parameters. Here each variable was set above. "True" is 'do_create_BE_waveform', 
        # if we set 'do_create_BE_waveform' to "False", we will only input above parameters into PyAE
        self.VI.setcontrolvalue('BE_pulse_control_cluster', 
                                ((be_parms_list[0])*1000, 
                                 (be_parms_list[1])*1000, 
                                 be_parms_list[2],
                                 be_parms_list[3], be_parms_list[4], 
                                 (be_parms_list[5])/1000, 
                                 be_parms_list[6], 
                                 (be_parms_list[7])*1000, 
                                 (be_parms_list[8])/1000, do_create_be_waveform))
        
        # Get BE pulse cluster. We can get (and save) BE pulse parameters for post measurement analysis
        if feedbackon == True:
            time.sleep(0.5)
            be_parms = self.VI.getcontrolvalue('BE_pulse_control_cluster')
            print("BE parameters are: ", be_parms[:-1])
            print("Please reset if some parameters are incorrect")
            return be_parms[:-1]
        else:
            return

    def define_apply_pulse(self, pulse_parms_dict = None, 
                           do_create_pulse = True, do_upload_pulse = True, do_apply_pulse = True,
                           feedbackon = True):
        """
        pulse_parms_dict: dictionary of DC pulse parameters
        e.g., pulse_parms_dict = {"pulse_init_amplitude_V_00": 3}
        Default parameters are the values shown on the panel now 
        """
        # Get default values
        default_pulse_parms = self.VI.getcontrolvalue("voltage_pulse_control_cluster")

        pulse_parms_list = [default_pulse_parms[0], default_pulse_parms[1],
                            default_pulse_parms[2], default_pulse_parms[3], 
                            default_pulse_parms[4], default_pulse_parms[5],
                            default_pulse_parms[6]]
        pulse_parms_name_list = ['pulse_init_amplitude_V_00', 'pulse_mid_amplitude_V_01',
                                 'pulse_final_amplitude_V_02', 'pulse_on_duration_s_03', 
                                 'pulse_final_duration_s_04', 'rise_time_s_05',
                                 'pulse_repeats_06']
        # if user customized some parameters, set the parameters as customized values
        if pulse_parms_dict != None:
            for i in range (len (pulse_parms_list)):
                if pulse_parms_name_list[i] in pulse_parms_dict:
                    pulse_parms_list[i] = pulse_parms_dict[pulse_parms_name_list[i]]
        
        ## Set pulse control value
        self.VI.setcontrolvalue('voltage_pulse_control_cluster', 
                                (pulse_parms_list[0], pulse_parms_list[1], pulse_parms_list[2],
                                 pulse_parms_list[3], pulse_parms_list[4], pulse_parms_list[5],
                                 pulse_parms_list[6], do_create_pulse, False, False))
        ## Wait until pulse is created
        while self.VI.getcontrolvalue('voltage_pulse_control_cluster')[7]:
            time.sleep(0.1) # wait 0.1 s and check status again

        ## Upload pulse
        self.VI.setcontrolvalue('voltage_pulse_control_cluster', 
                                (pulse_parms_list[0], pulse_parms_list[1], pulse_parms_list[2],
                                 pulse_parms_list[3], pulse_parms_list[4], pulse_parms_list[5],
                                 pulse_parms_list[6], False, do_upload_pulse, False))
        ## Wait until pulse is uploaded
        while self.VI.getcontrolvalue('voltage_pulse_control_cluster')[8]:
            time.sleep(0.1) # wait 0.1 s and check status again
        
        ## Apply pulse
        self.VI.setcontrolvalue('voltage_pulse_control_cluster', 
                                (pulse_parms_list[0], pulse_parms_list[1], pulse_parms_list[2],
                                 pulse_parms_list[3], pulse_parms_list[4], pulse_parms_list[5],
                                 pulse_parms_list[6], False, False, do_apply_pulse))
        ## Wait until pulse is created
        while self.VI.getcontrolvalue('voltage_pulse_control_cluster')[9]:
            time.sleep(0.1) # wait 0.1 s and check status again

        # Get pulse parameters
        if feedbackon == True:
            time.sleep(0.2)
            pulse_parameters = self.VI.getcontrolvalue("voltage_pulse_control_cluster")
            print("pulse parameters are: ", pulse_parameters[:-3])

        return 
    
    def do_line_scan(self, line_scan_parms_dict = None, upload_to_daq = False, do_line_scan = False, feedbackon = True):
        """
        line_scan_parms_dict: dictionary of BE line scan control cluster parameters
        e.g., line_scan_parms_dict = {"voltage_offest_V_00": 0, "num_BE_pulse_01": 128, 
        "do_upload_to_DAQ_02": True, "start_x_pos_00": 0, "start_y_pos_01": 0, 
        "stop_x_pos_02": 1, "stop_y_pos_03": 0, "do_BE_line_scan_04": True}
        Default parameters are the values shown in the panel now    
        """
        # Get default values
        default_line_scan_parms_1 = self.VI.getcontrolvalue("Initialize_BE_line_scan_control_cluster")
        default_line_scan_parms_2 = self.VI.getcontrolvalue("BE_line_scan_control_cluster")
        
        # Set default values
        linescan_parms_list = [default_line_scan_parms_1[0], default_line_scan_parms_1[1], default_line_scan_parms_2[0], 
                               default_line_scan_parms_2[1], default_line_scan_parms_2[2], default_line_scan_parms_2[3]]
        linescan_parms_name_list = ["voltage_offest_V_00", "num_BE_pulses_01", "start_x_pos_00",
                                    "start_y_pos_01", "stop_x_pos_02", "stop_y_pos_03"]
        
        # if user customized some parameters, set the parameters as customized values
        if line_scan_parms_dict != None:
            for i in range (len (linescan_parms_list)):
                if linescan_parms_name_list[i] in line_scan_parms_dict:
                    linescan_parms_list[i] = line_scan_parms_dict[linescan_parms_name_list[i]]
        
        if upload_to_daq == True:
            ## Set line scan control cluster
            self.VI.setcontrolvalue('Initialize_BE_line_scan_control_cluster', 
                                    (linescan_parms_list[0], linescan_parms_list[1], upload_to_daq))
            # Wait until linescan waveform is uploaded to daq card
            while self.VI.getcontrolvalue('Initialize_BE_line_scan_control_cluster')[2]:
                time.sleep(0.1) # wait 0.1 s and check the status again

            time.sleep(2)    
        
            ## Set line scan control cluster
            self.VI.setcontrolvalue('Initialize_BE_line_scan_control_cluster', 
                                    (linescan_parms_list[0], linescan_parms_list[1], upload_to_daq))
            # Wait until linescan waveform is uploaded to daq card
            while self.VI.getcontrolvalue('Initialize_BE_line_scan_control_cluster')[2]:
                time.sleep(0.1) # wait 0.1 s and check the status again
        

        ## Set BE line scan control cluster
        self.VI.setcontrolvalue('BE_line_scan_control_cluster', 
                                (linescan_parms_list[2], linescan_parms_list[3], 
                                 linescan_parms_list[4], linescan_parms_list[5],
                                 do_line_scan))
        # Wait until linescan is finished
        while self.VI.getcontrolvalue('BE_line_scan_control_cluster')[4]:
            time.sleep(0.1) # wait 0.1 s and check the status again
        
        # feedback about parameters
        if feedbackon == True:
            line_scan_parms_1 = self.VI.getcontrolvalue('Initialize_BE_line_scan_control_cluster')
            line_scan_parms_2 = self.VI.getcontrolvalue('BE_line_scan_control_cluster')
            print ("voltage offset and number of BE pulse are: ", line_scan_parms_1[:-1])
            print ("line scan start and end positions: ", line_scan_parms_2[:-1])

        ## Get BE line data
        be_line_result = self.VI.getcontrolvalue("BE_line_scan_indicator_cluster")
        complex_spectrogram = be_line_result[1]
        sho_guess_cluster = be_line_result[3]
        channel1 = be_line_result[4]
        channel2 = be_line_result[5]
        channel3 = be_line_result[6]

        return complex_spectrogram, sho_guess_cluster, channel1, channel2, channel3  #return raw data and quick fitting

    def raster_scan(self, file_name = "BEPFM", raster_parms_dict = None, 
                    fit = False, feedbackon = False, progress_on = True, plot_on = True):
        """Perform a raster BE scan
        raster_parms_dict: dictionary of BE raster scan paramters
        e.g., raster_parms_dict = {"tip_voltage": 0, "scan_pixel": 128, "scan_x_range": [-1, 1]}
        Default parameters are the values shown in the panel now   
        """
        # Get default value
        line_scan_parms_1 = self.VI.getcontrolvalue("Initialize_BE_line_scan_control_cluster")
        line_scan_parms_2 = self.VI.getcontrolvalue("BE_line_scan_control_cluster")

        # Set default parameters
        raster_parms_name_list = ["tip_voltage", "scan_pixel", "scan_x_start", "scan_y_start", "scan_x_stop", "scan_y_stop"]
        raster_parms_list = [line_scan_parms_1[0], line_scan_parms_1[1], line_scan_parms_2[0], 
                             line_scan_parms_2[1], line_scan_parms_2[2], line_scan_parms_2[3]]

         # if user customized some parameters, set the parameters as customized values
        if raster_parms_dict !=None:
            for i in range (len (raster_parms_list)):
                if raster_parms_name_list[i] in raster_parms_dict:
                    raster_parms_list[i] = raster_parms_dict[raster_parms_name_list[i]]

        raster_quick_fit = []
        raster_channel1 = []
        raster_channel2 = []
        raster_channel3 = []
        raster_complex_spectra = []

        scan_line_array = np.linspace(raster_parms_list[3], raster_parms_list[5], raster_parms_list[1])

        self.tip_control(tip_parms_dict = {"next_x_pos_00": raster_parms_list[2], 
                                           "next_y_pos_01": scan_line_array[0]}, feedbackon = feedbackon)
        # whiel tip is moving
        # Upload BE excitation waveform to DAQ
        self.do_line_scan(line_scan_parms_dict = {"voltage_offset_V_00": raster_parms_list[0], 
                                                  "num_BE_pulses_01": raster_parms_list[1]},
                                                  upload_to_daq = True, feedbackon = feedbackon)
        # Wait until waveform is uploaded to daq
        while self.VI.getcontrolvalue('Initialize_BE_line_scan_control_cluster')[2]:
            time.sleep(0.1) # wait 0.1 s and check the status again 
        
        # make a progress bar
        if progress_on:
            bar_progress = self.progress_bar(int(raster_parms_list[1]))  
        for i in range(int(raster_parms_list[1])):
            # Move tip to strat pos
            self.tip_control(tip_parms_dict = {"next_x_pos_00": raster_parms_list[2], 
                                               "next_y_pos_01": scan_line_array[i], 
                                               "transit_time_s_02": 0.5}, do_set_setpoint = False, feedbackon = feedbackon)
            # While tip is moving, wait until tip move is done
            while self.VI.getcontrolvalue('move_tip_control_cluster')[3]:
                time.sleep(0.1)  # Wait 0.1 s and check if action is done again

            line_cx_spectra, line_quick_fit, line_channel1, line_channel2, line_channel3= self.do_line_scan(
                line_scan_parms_dict = {"start_x_pos_00": raster_parms_list[2],
                                        "start_y_pos_01": scan_line_array[i], "stop_x_pos_02": raster_parms_list[4],
                                        "stop_y_pos_03": scan_line_array[i]}, do_line_scan = True, feedbackon = feedbackon)
            
            raster_quick_fit.append(np.asarray(line_quick_fit))
            raster_channel1.append(line_channel1)
            raster_channel2.append(line_channel2)
            raster_channel3.append(line_channel3)
            raster_complex_spectra.append(np.asarray(line_cx_spectra))

            # plot real time images
            if plot_on == True:
                if i%5 == 0:
                    clear_output(wait=True)
                    fig, axs = plt.subplots(1, 7, figsize=(28, 4))
                    fig.subplots_adjust(left=0.02, bottom=0.06, right=0.95, top=0.94, wspace=0.2)
                    cm = 'viridis'
                    shrink = 0.8
                    # channel 1
                    im0 = axs[0].imshow(np.asarray(raster_channel1), interpolation='nearest', cmap=cm)
                    fig.colorbar(im0, ax=axs[0], shrink = shrink, label = "Channel 1 (a.u.)")
                    axs[0].axis('off')
                    # channel 2
                    im1 = axs[1].imshow(np.asarray(raster_channel2), interpolation='nearest', cmap=cm)
                    fig.colorbar(im1, ax=axs[1], shrink = shrink, label = "Channel 2 (a.u.)")
                    axs[1].axis('off')
                    # channel 3
                    im2 = axs[2].imshow(np.asarray(raster_channel3), interpolation='nearest', cmap=cm)
                    fig.colorbar(im2, ax=axs[2], shrink = shrink, label = "Channel 3 (a.u.)")
                    axs[2].axis('off')
                    # amplitude
                    im3 = axs[3].imshow((np.asarray(raster_quick_fit))[:,:,0], interpolation='nearest', cmap=cm)
                    fig.colorbar(im3, ax=axs[3], shrink = shrink, label = "Amplitude (a.u.)")
                    axs[3].axis('off')
                    # frequency
                    im4 = axs[4].imshow(((np.asarray(raster_quick_fit))[:,:,1])/1000, interpolation='nearest', cmap=cm)
                    fig.colorbar(im4, ax=axs[4], shrink = shrink, label = "Frequency (kHz)")
                    axs[4].axis('off')
                    # q factor
                    im5 = axs[5].imshow((np.asarray(raster_quick_fit))[:,:,2], interpolation='nearest', cmap=cm)
                    fig.colorbar(im5, ax=axs[5], shrink = shrink, label = "Q factor (a.u.)")
                    axs[5].axis('off')
                    # phase
                    im6 = axs[6].imshow((np.asarray(raster_quick_fit))[:,:,3], interpolation='nearest', cmap=cm)
                    fig.colorbar(im6, ax=axs[6], shrink = shrink, label = "Phase (rad)")
                    axs[6].axis('off')
                    plt.show()

            # update progress
            if progress_on:
                bar_progress.update(i)

        dset_imgs, dset_chns, complex_spectra = self.mk_dset(file_name = file_name, 
                                                             pfm_imgstack = np.asarray(raster_quick_fit),
                                                             channel_imgstack = np.asarray([raster_channel1, raster_channel2, raster_channel3]),
                                                             complex_spectra = np.asarray(raster_complex_spectra),
                                                             start_x = raster_parms_list[2], finish_x = raster_parms_list[4],
                                                             start_y = raster_parms_list[3], finish_y = raster_parms_list[5])

        # return raster_quick_fit, raster_complex_spectra, raster_channel1, raster_channel2, line_channel3
        return dset_imgs, dset_chns, complex_spectra
    

    def define_BEPS_parameters(self, beps_parms_dict = None, do_create_waveform = False, 
                               do_upload_waveform = False, do_VS_waveform = False, feedbackon = True):
        """
        beps_parms_dict: dictionary of BEPS measurement parameters
        e.g., beps_parms_dict = {"amplitude_V_00": 6, "steps_per_cycles_03": 64, 
        "num_cycles_04": 3, "measure_loops_07": 0}
        do_create_waveform: create a waveform; do_upload_waveform: upload waveform to DAQ; do_VS_waveform: output waveform
        Notes: cycle_fraction_05: index 0 is full, index 1 is 3/4, index 2 is 1/2, index 3 is 1/4; 
        cycle_phase_shift_06: index 0 is 0, index 1 is 1/4, index 2 is 1/2, index 4 is 3/4;
        measure_loops_07: index 0 is on-and-off-field, index 1 is on-field-only.
        Default:    
        """
        # Get default parameters
        default_beps_parms = self.VI.getcontrolvalue("Initialize_BEPS_VS_control_cluster")
        
        # Set default parameters
        beps_parms_list = [default_beps_parms[0], default_beps_parms[1], default_beps_parms[2], default_beps_parms[3],
                           default_beps_parms[4], default_beps_parms[5], default_beps_parms[6], default_beps_parms[7],
                           default_beps_parms[8], default_beps_parms[9], default_beps_parms[10], default_beps_parms[11], 
                           default_beps_parms[12], default_beps_parms[13], default_beps_parms[14], default_beps_parms[15],
                           default_beps_parms[16], default_beps_parms[17]]
        beps_parms_name_list = ["amplitude_V_00", "offset_V_01", "read_voltage_V_02", "step_per_cycle_03",
                                "num_cycles_04", "cycle_fraction_05", "cycle_phase_shift_06", "measure_loops_07",
                                "transition_time_s_08", "delay_after_step_s_09", "set_pulse_amplitude_V_10", 
                                "set_pulse_duration_s_11", "FORC_num_cycles_12", "FORC_A1_V_13", "FORC_A2_V_14",
                                "FORC_num_repeats_15", "FORC_B1_V_16", "FORC_B2_V_17"] 
        # if user customized some parameters, set the parameters as customized values
        if beps_parms_dict != None:
            for i in range (len (beps_parms_list)):
                if beps_parms_name_list[i] in beps_parms_dict:
                    beps_parms_list[i] = beps_parms_dict[beps_parms_name_list[i]]

        ## Set BEPS control cluster
        self.VI.setcontrolvalue('Initialize_BEPS_VS_control_cluster', 
                                (beps_parms_list[0], beps_parms_list[1], beps_parms_list[2], beps_parms_list[3], 
                                 beps_parms_list[4], beps_parms_list[5], beps_parms_list[6], beps_parms_list[7], 
                                 beps_parms_list[8], beps_parms_list[9], beps_parms_list[10], beps_parms_list[11],
                                 beps_parms_list[12], beps_parms_list[13], beps_parms_list[14], beps_parms_list[15], 
                                 beps_parms_list[16], beps_parms_list[17], 
                                 do_create_waveform, False, False))
        # Wait until waveform is created
        while self.VI.getcontrolvalue('Initialize_BEPS_VS_control_cluster')[18]:
            time.sleep(0.1)

        self.VI.setcontrolvalue('Initialize_BEPS_VS_control_cluster', 
                                (beps_parms_list[0], beps_parms_list[1], beps_parms_list[2], beps_parms_list[3], 
                                 beps_parms_list[4], beps_parms_list[5], beps_parms_list[6], beps_parms_list[7], 
                                 beps_parms_list[8], beps_parms_list[9], beps_parms_list[10], beps_parms_list[11],
                                 beps_parms_list[12], beps_parms_list[13], beps_parms_list[14], beps_parms_list[15], 
                                 beps_parms_list[16], beps_parms_list[17], 
                                 False, do_upload_waveform, False))
        while self.VI.getcontrolvalue('Initialize_BEPS_VS_control_cluster')[19]:
            time.sleep(0.1)
    
        self.VI.setcontrolvalue('Initialize_BEPS_VS_control_cluster', 
                                (beps_parms_list[0], beps_parms_list[1], beps_parms_list[2], beps_parms_list[3], 
                                 beps_parms_list[4], beps_parms_list[5], beps_parms_list[6], beps_parms_list[7], 
                                 beps_parms_list[8], beps_parms_list[9], beps_parms_list[10], beps_parms_list[11],
                                 beps_parms_list[12], beps_parms_list[13], beps_parms_list[14], beps_parms_list[15], 
                                 beps_parms_list[16], beps_parms_list[17], 
                                 False, False, do_VS_waveform))
        while self.VI.getcontrolvalue('Initialize_BEPS_VS_control_cluster')[20]:
            time.sleep(0.1)

        # Show BEPS parameters
        if feedbackon == True:
            beps_parms = self.VI.getcontrolvalue("Initialize_BEPS_VS_control_cluster")
            print("BEPS parameters are: ", beps_parms)
        
        if do_VS_waveform == True:
            ## Get BEPS data
            beps_result = self.VI.getcontrolvalue("BEPS_VS_indicator_cluster")
            beps_vs_vec = beps_result[0]
            beps_cpx_spectrogram = beps_result[1]
            beps_amp_vec = beps_result[2]
            beps_res_vec = beps_result[3]
            beps_Q_vec = beps_result[4]
            beps_pha_vec = beps_result[5]
            beps_ch01 = beps_result[7]
            beps_ch02 = beps_result[8]
            beps_ch03 = beps_result[9]
        
            #return raw data and quick fitting
            return beps_vs_vec, beps_cpx_spectrogram, [beps_amp_vec,beps_res_vec, beps_Q_vec,
                                                       beps_pha_vec], [beps_ch01, beps_ch02, beps_ch03]  
        else:
            return 

    def do_beps (self, beps_parms_dict = None, beps_grid_parms_dict = None, file_name = "BEPS", 
                      type = "grid", counts = 10, coordinates = None, feedbackon = False, progress_on = True):
        """Define grid points beps measurements
        beps_parms_dict: dictionary of BEPS measurement parameters 
        e.g., beps_parms_dict = {"amplitude_V_00": 6, "steps_per_cycles_03": 64, 
        "num_cycles_04": 3, "measure_loops_07": 0, "do_create_VS_waveform_18": True, "do_upload_VS_waveform_19": True,
        "do_VS_waveform_20": True}

        beps_grid_parms_dict: dictionary for grid beps parameters, default values:
         range_x = [-1, 1], range_y = [-1, 1], pixel_num_x = 10, pixel_num_y = 10
        e.g., beps_grid_parms_dict{"pixel_x": 10, "pixel_y": 10}
        By default, this function performs grid beps. However, (1) we can also perform BEPS at random locations 
        by setting type = "random" and providing "counts", "counts" means how many random location we would like to measure. (2) we can also 
        perform BEPS at specific locations by setting type = "specific" and providing the "coordinates"
        """
        
        # Set default value
        self.range_x = [-1, 1]
        self.range_y = [-1, 1]
        self.pixel_num_x = 5
        self.pixel_num_y = 5

        beps_grid_parms_list = [self.range_x, self.range_y, self.pixel_num_x, self.pixel_num_y]
        beps_grid_parms_name_list = ["range_x", "range_y", "pixel_num_x", "pixel_num_y"]
        # if user customized some parameters, set the parameters as customized values
        if beps_grid_parms_dict != None:
            for i in range (len (beps_grid_parms_list)):
                if beps_grid_parms_name_list[i] in beps_grid_parms_dict:
                    beps_grid_parms_list[i] = beps_grid_parms_dict[beps_grid_parms_name_list[i]]
        
        # Define grid locations
        pixel_x = np.linspace(beps_grid_parms_list[0][0], beps_grid_parms_list[0][1], beps_grid_parms_list[2])
        pixel_y = np.linspace(beps_grid_parms_list[1][0], beps_grid_parms_list[1][1], beps_grid_parms_list[3])
        pixels_xy = np.meshgrid(pixel_x, pixel_y)
        pixels_x = pixels_xy[0].reshape(-1)
        pixels_y = pixels_xy[1].reshape(-1)

        if type == "grid":  # grid measurements
            coordinates_final = np.asarray([pixels_x, pixels_y])

        elif type == "random":   # measure random locations
            coordinates_index = np.random.choice(len(pixels_x), counts, replace=False)
            pixels_x = pixels_x[coordinates_index]
            pixels_y = pixels_y[coordinates_index]
            coordinates_final = np.asarray([pixels_x, pixels_y])

        elif type == "specific":   # User input specific coordinates
            # coordinates_index = (self.pixel_num_y)*coordinates[1] + coordinates[0]
            pixels_x = np.asarray([pixel_x[coordinates[0]]])
            pixels_y = np.asarray([pixel_y[coordinates[0]]])
            coordinates_final = np.asarray([pixels_x[0], pixels_y[0]])

        # Upload BEPS waveform
        self.define_BEPS_parameters(beps_parms_dict = beps_parms_dict, do_create_waveform = True, 
                                    do_upload_waveform = True, do_VS_waveform = False, feedbackon = False)
        # creat an emapy list to save data
        grid_beps_quick_fit = []
        grid_beps_cpx_spectra = []
        grid_beps_chns = []

        # make a progress bar
        if progress_on:
            bar_progress = self.progress_bar(max_value = len(pixels_x))

        for i in range(len(pixels_x)):
            # move tip 
            self.tip_control(tip_parms_dict={"next_x_pos_00": pixels_x[i],
                                             "next_y_pos_01": pixels_y[i], 
                                             "transit_time_s_02": 0.2},
                                             do_move_tip = True, do_set_setpoint = False, 
                                             feedbackon=feedbackon)
            time.sleep(0.1)
            # do BEPS
            vs, cpx_spectra, beps_quick_fit, beps_chns = self.define_BEPS_parameters(beps_parms_dict = None,
                                                                                     do_create_waveform = False,
                                                                                     do_upload_waveform = False, 
                                                                                     do_VS_waveform = True, feedbackon=feedbackon)

            grid_beps_quick_fit.append(beps_quick_fit)
            grid_beps_cpx_spectra.append(cpx_spectra)
            grid_beps_chns.append(beps_chns)

            #update progress
            if progress_on:
                bar_progress.update(i)

        vdc, beps_qf, beps_chs, beps_cs = self.mk_dset(file_name = file_name,
                                                       pfm_imgstack = np.asarray(grid_beps_quick_fit),
                                                       channel_imgstack = np.asarray(grid_beps_chns),
                                                       complex_spectra = np.asarray(grid_beps_cpx_spectra),
                                                       start_x = beps_grid_parms_list[0][0],
                                                       finish_x = beps_grid_parms_list[0][1],
                                                       start_y = beps_grid_parms_list[1][0], 
                                                       finish_y = beps_grid_parms_list[1][1], 
                                                       coordinates = coordinates_final,
                                                       beps = True)

        return vdc, beps_qf, beps_chs, beps_cs   # return BEPS dc waveform and grid beps results
    
    def fpga_spiral_scan(self, spiral_parms_dict = None, scan_type = 2, data_rate = 0, do_scan_update = True, 
                    scan_x_offset = 0, scan_y_offset = 0, scan_rotation_deg = 0, do_scan = False, feedbackon = True):
        """Define spiral scan parameters
        spiral_parms_dict: dictionary of spiral scan parameters 
        e.g., spiral_parms_dict = {"spiral_inner_radius_x_V_00": 0, "spiral_outer_radius_x_V_01": 1, 
        "spiral_inner_radius_y_V_02": 0, "spiral_outer_radius_y_V_03": 1, "sprial_N_cycles_04": 10, "spiral_duration_05": 100E-3,
        "spiral_direction_07": 0, "spiral_return_opt_08": 0}

        Default parameters are the values shown in the panel now.
        """
        # Set scan type to spiral scan
        self.VIs.setcontrolvalue("scan_type", (scan_type))
        # Set data rate
        self.VIs.setcontrolvalue("data_rate", (data_rate))

        # Get default value
        spiral_parms = self.VIs.getcontrolvalue("spiral_scan_control_cluster")
        
        spiral_parms_list = [spiral_parms[0], spiral_parms[1], spiral_parms[2], 
                             spiral_parms[3], spiral_parms[4], spiral_parms[5], spiral_parms[6],
                             spiral_parms[7], spiral_parms[8]]
        spiral_parms_name_list = ["spiral_inner_radius_x_V_00", "spiral_outer_radius_x_V_01", "spiral_inner_radius_y_V_02",
                                  "spiral_outer_radius_y_V_03", "spiral_N_cycles_04", "spiral_duration_05", "spiral_dose_distrituion_06",
                                  "spiral_direction_07", "spiral_return_opt_08"]
        
        # if user customized some parameters, set the parameters as customized values
        if spiral_parms_dict != None:
            for i in range (len (spiral_parms_list)):
                if spiral_parms_name_list[i] in spiral_parms_dict:
                    spiral_parms_list[i] = spiral_parms_dict[spiral_parms_name_list[i]]

        ## Set spiral scan control cluster
        self.VIs.setcontrolvalue('spiral_scan_control_cluster', 
                                (spiral_parms_list[0], spiral_parms_list[1], spiral_parms_list[2], spiral_parms_list[3],
                                 spiral_parms_list[4], spiral_parms_list[5], spiral_parms_list[6], spiral_parms_list[7],
                                 spiral_parms_list[8]))
        
        # Updata spiral scan parameters
        self.VIs.setcontrolvalue("do_scan_update", (do_scan_update))
        # Wait until spiral scan parameters are updated
        while self.VIs.getcontrolvalue("do_scan_update"):
            time.sleep(0.1) # wait 0.1 s and check the status again

        # Set scan offset and rotation angle
        self.VIs.setcontrolvalue("scan_x_offset_V", (scan_x_offset))
        self.VIs.setcontrolvalue("scan_y_offset_V", (scan_y_offset))
        self.VIs.setcontrolvalue("scan_rotation_deg", (scan_rotation_deg))
        
        # Do spiral scan
        self.VIs.setcontrolvalue("do_scan", (do_scan))
        # Wait until sprial scan is done
        while self.VIs.getcontrolvalue("do_scan"):
            time.sleep(0.1)

        time.sleep(0.5)

        # Get results
        mask = self.VIs.getcontrolvalue("image_mask")
        counts = self.VIs.getcontrolvalue("image_counts")
        image_AI0 = self.VIs.getcontrolvalue("image_AI0")
        image_AI1 = self.VIs.getcontrolvalue("image_AI1")
        image_AI2 = self.VIs.getcontrolvalue("image_AI2")
        image_AI3 = self.VIs.getcontrolvalue("image_AI3")

        results = {"mask": mask, "counts": counts, "image_AI0": image_AI0, 
                   "image_AI1": image_AI1, "image_AI2": image_AI2, "image_AI3": image_AI3}

        return results
    
    def fpga_raster_scan(self, fpga_raster_parms_dict = None, scan_type = 3, data_rate = 0, do_scan_update = True, 
                    scan_x_offset = 0, scan_y_offset = 0, scan_rotation_deg = 0, do_scan = False):
        """Define spiral scan parameters
        fpga_raster_parms_dict: dictionary of raster scan parameters 
        e.g., fpga_raster_parms_dict = {"raster_scan_size_x_V_00": 1, "raster_scan_size_y_V_01": 1,
        "raster_N_scan_lines_02": 64, "raster_scan_duration_s_03": 100E-3, "raster_type_04": 0}

        default parameters are the values shown in the panel
        """
        # Set scan type to raster scan
        self.VIs.setcontrolvalue("scan_type", (scan_type))
        # Set data rate
        self.VIs.setcontrolvalue("data_rate", (data_rate))

        # Set default value
        raster_scan_size_x_V_00 = 1,
        raster_scan_size_y_V_01 = 1,
        raster_N_scan_lines_02 = 64 
        raster_scan_duration_s_03 = 100E-3
        raster_type_04 = 0
        
        fpga_raster_parms_list = [raster_scan_size_x_V_00, raster_scan_size_y_V_01, raster_N_scan_lines_02, 
                                  raster_scan_duration_s_03, raster_type_04]
        fpga_raster_parms_name_list = ["raster_scan_size_x_V_00", "raster_scan_size_y_V_01", "raster_N_scan_lines_02",
                                       "raster_scan_duration_s_03", "raster_type_04"]
        
        # if user customized some parameters, set the parameters as customized values
        if fpga_raster_parms_dict != None:
            for i in range (len (fpga_raster_parms_list)):
                if fpga_raster_parms_name_list[i] in fpga_raster_parms_dict:
                    fpga_raster_parms_list[i] = fpga_raster_parms_dict[fpga_raster_parms_name_list[i]]

        ## Set raster scan control cluster
        self.VIs.setcontrolvalue('fast_raster_scan_control_cluster', 
                                (fpga_raster_parms_list[0], fpga_raster_parms_list[1], fpga_raster_parms_list[2], 
                                 fpga_raster_parms_list[3], fpga_raster_parms_list[4]))
        
        # Updata raster scan parameters
        self.VIs.setcontrolvalue("do_scan_update", (do_scan_update))
        # Wait until scan parameters are updated
        while self.VIs.getcontrolvalue("do_scan_update"):
            time.sleep(0.1) # wait 0.1 s and check the status again

        # Set scan offset and rotation angle
        self.VIs.setcontrolvalue("scan_x_offset_V", (scan_x_offset))
        self.VIs.setcontrolvalue("scan_y_offset_V", (scan_y_offset))
        self.VIs.setcontrolvalue("scan_rotation_deg", (scan_rotation_deg))
        
        # Do raster scan
        self.VIs.setcontrolvalue("do_scan", (do_scan))
        # Wait until raster scan is done
        while self.VIs.getcontrolvalue("do_scan"):
            time.sleep(0.1)

        # Get results
        mask = self.VIs.getcontrolvalue("image_mask")
        counts = self.VIs.getcontrolvalue("image_counts")
        image_AI0 = self.VIs.getcontrolvalue("image_AI0")
        image_AI1 = self.VIs.getcontrolvalue("image_AI1")
        image_AI2 = self.VIs.getcontrolvalue("image_AI2")
        image_AI3 = self.VIs.getcontrolvalue("image_AI3")

        results = {"mask": mask, "counts": counts, "image_AI0": image_AI0, 
                   "image_AI1": image_AI1, "image_AI2": image_AI2, "image_AI3": image_AI3}

        return results
    

    def fpga_spiral_scan_BE(self, be_parms_dict = None, do_create_be_waveform = True,
                            spiral_parms_dict = None, num_BE_pulse = 128, tip_voltage = 0, 
                            scan_type = 2, data_rate = 0, do_scan_update = True,
                            scan_x_offset = 0, scan_y_offset = 0, scan_rotation_deg = 0,
                            do_BE_arb_line_update_00 = True, do_BE_arb_line_scan_01 = True):
        # define be parameters first
        self.define_be_parms(be_parms_dict = be_parms_dict, do_create_be_waveform = do_create_be_waveform)
        
        # define spiral parameters
        self.fpga_spiral_scan(spiral_parms_dict = spiral_parms_dict, scan_type = scan_type, 
                              data_rate = data_rate, do_scan_update = do_scan_update,  # do scan update can be False 
                              scan_x_offset = scan_x_offset, scan_y_offset = scan_y_offset,
                              scan_rotation_deg = scan_rotation_deg, do_scan = False)  # do scan need to be False here, scan will be triggered from PyAe side
        # upload be scan pulse to DAQ
        self.VI.setcontrolvalue("initialize_BE_line_scan_control_cluster", (tip_voltage, num_BE_pulse, True))
        # Wait when uploading pulse
        while self.VI.setcontrolvalue("initialize_BE_line_scan_control_cluster")[2] == True:
            time.sleep(0.1)
        time.sleep(1)

        # upload be scan pulse to DAQ
        self.VI.setcontrolvalue("initialize_BE_line_scan_control_cluster", (tip_voltage, num_BE_pulse, True))
        # Wait when uploading pulse
        while self.VI.setcontrolvalue("initialize_BE_line_scan_control_cluster")[2] == True:
            time.sleep(0.1)
        time.sleep(1)

        # update BE arb scan
        self.VI.setcontrolvalue("BE_arb_scan_control_cluster", (False, do_BE_arb_line_update_00))
        # wait until update finish
        while self.VI.getcontrolvalue("BE_arb_scan_control_cluster")[0]:
            time.sleep(0.1)
        
        # do BE arb scan
        self.VI.setcontrolvalue("BE_arb_scan_control_cluster", (do_BE_arb_line_scan_01, False))
        # wait until scan finish
        while self.VI.getcontrolvalue("BE_arb_scan_control_cluster")[1]:
            time.sleep(0.1)
        
        # Wait until raster scan is done
        while self.VIs.getcontrolvalue("do_scan"):
            time.sleep(0.1)
            
        # get BE results
        be_result = self.VI.getcontrolvalue("BE_line_scan_indicator_cluster")
        complex_spectrogram, sho_guess_cluster = be_result[1], be_result[3]
        
        # Get fpga results
        mask = self.VIs.getcontrolvalue("image_mask")
        counts = self.VIs.getcontrolvalue("image_counts")
        image_AI0 = self.VIs.getcontrolvalue("image_AI0")
        image_AI1 = self.VIs.getcontrolvalue("image_AI1")
        image_AI2 = self.VIs.getcontrolvalue("image_AI2")
        image_AI3 = self.VIs.getcontrolvalue("image_AI3")

        fpga_results = {"mask": mask, "counts": counts, "image_AI0": image_AI0, 
                   "image_AI1": image_AI1, "image_AI2": image_AI2, "image_AI3": image_AI3}
        
        return complex_spectrogram, sho_guess_cluster, fpga_results

        
    def fpga_raster_scan_BE(self, be_parms_dict = None, do_create_be_waveform = True,
                            fpga_raster_parms_dict = None, num_BE_pulse = 128, tip_voltage = 0, 
                            scan_type = 3, data_rate = 0, 
                            do_scan_update = True, scan_x_offset = 0, scan_y_offset = 0, scan_rotation_deg = 0,
                            do_BE_arb_line_update_00 = True, do_BE_arb_line_scan_01 = True):
        # define be parameters first
        self.define_be_parms(be_parms_dict = be_parms_dict, do_create_be_waveform = do_create_be_waveform)
        
        # define spiral parameters
        self.fpga_raster_scan(fpga_raster_parms_dict = fpga_raster_parms_dict, scan_type = scan_type,
                              data_rate = data_rate, do_scan_update = do_scan_update,  # do scan update can be False
                              scan_x_offset = scan_x_offset, scan_y_offset = scan_y_offset,
                              scan_rotation_deg = scan_rotation_deg, do_scan = False)  # do scan need to be False here, scan will be triggered from PyAe side
        
        # upload be scan pulse to DAQ
        self.VI.setcontrolvalue("initialize_BE_line_scan_control_cluster", (tip_voltage, num_BE_pulse, True))
        # Wait when uploading pulse
        while self.VI.setcontrolvalue("initialize_BE_line_scan_control_cluster")[2] == True:
            time.sleep(0.1)
        time.sleep(1)

        # upload be scan pulse to DAQ
        self.VI.setcontrolvalue("initialize_BE_line_scan_control_cluster", (tip_voltage, num_BE_pulse, True))
        # Wait when uploading pulse
        while self.VI.setcontrolvalue("initialize_BE_line_scan_control_cluster")[2] == True:
            time.sleep(0.1)
        time.sleep(1)

        # update BE arb scan
        self.VI.setcontrolvalue("BE_arb_scan_control_cluster", (False, do_BE_arb_line_update_00))
        # wait until update finish
        while self.VI.getcontrolvalue("BE_arb_scan_control_cluster")[0]:
            time.sleep(0.1)
        
        # do BE arb scan
        self.VI.setcontrolvalue("BE_arb_scan_control_cluster", (do_BE_arb_line_scan_01, False))
        # wait until scan finish
        while self.VI.getcontrolvalue("BE_arb_scan_control_cluster")[1]:
            time.sleep(0.1)
            
        # Wait until raster scan is done
        while self.VIs.getcontrolvalue("do_scan"):
            time.sleep(0.1)
            
        # get BE results
        be_result = self.VI.getcontrolvalue("BE_line_scan_indicator_cluster")
        complex_spectrogram, sho_guess_cluster = be_result[1], be_result[3]

        # Get fpga results
        mask = self.VIs.getcontrolvalue("image_mask")
        counts = self.VIs.getcontrolvalue("image_counts")
        image_AI0 = self.VIs.getcontrolvalue("image_AI0")
        image_AI1 = self.VIs.getcontrolvalue("image_AI1")
        image_AI2 = self.VIs.getcontrolvalue("image_AI2")
        image_AI3 = self.VIs.getcontrolvalue("image_AI3")

        fpga_results = {"mask": mask, "counts": counts, "image_AI0": image_AI0, 
                   "image_AI1": image_AI1, "image_AI2": image_AI2, "image_AI3": image_AI3}
        
        return complex_spectrogram, sho_guess_cluster, fpga_results

