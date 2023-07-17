Search.setIndex({"docnames": ["ht_workflows/ht", "ht_workflows/ht_domain_writing_analysis", "ht_workflows/ht_domain_writing_experiment", "intro", "python_guide/intro", "python_guide/introduction_notebook"], "filenames": ["ht_workflows\\ht.md", "ht_workflows\\ht_domain_writing_analysis.ipynb", "ht_workflows\\ht_domain_writing_experiment.ipynb", "intro.md", "python_guide\\intro.md", "python_guide\\introduction_notebook.ipynb"], "titles": ["High Throughput Experimentation", "Notebook for high throughput domain writing analysis", "High Throughput Domain Writing Workflow", "Welcome to AEcroscopy for Automated and Autonomous Microscopy", "Introduction to AEcroscopy", "Guide to Essential Commands and Functionalities in AEcroscopy"], "terms": {"thi": [0, 2, 3, 4, 5], "chapter": [0, 4, 5], "about": [0, 5], "experi": [0, 3, 4, 5], "workflow": [0, 3], "under": [0, 3], "construct": [0, 3], "we": [0, 1, 2, 3, 4, 5], "introduc": [0, 3, 4, 5], "here": [0, 2, 3, 4, 5], "_": [0, 3, 4], "yongtao": [0, 1, 2, 3, 4, 5], "liu": [0, 1, 2, 3, 4, 5], "june": [0, 1, 2, 3, 4, 5], "2023": [0, 1, 2, 3, 4, 5], "15": [1, 5], "you": [1, 2, 4, 5], "mai": [1, 2, 5], "need": [1, 2, 5], "sidpi": [1, 2, 5], "did": 1, "do": 1, "befor": [1, 5], "pip": 1, "instal": 1, "numpi": [1, 2, 5], "np": [1, 2, 5], "matplotlib": [1, 2, 5], "pyplot": [1, 2, 5], "plt": [1, 2, 5], "os": [1, 2, 5], "h5py": [1, 2, 5], "cv2": 1, "imutil": 1, "path": 1, "r": [1, 2, 5], "c": [1, 2, 5], "user": [1, 2, 3, 4, 5], "yla": [1, 2, 5], "dropbox": [1, 2, 5], "ornl": [1, 2, 5], "my": [1, 2, 5], "file": [1, 2, 5], "aecroscopy_bepya": [1, 2, 5], "aecroscopy_data": 1, "experiment1": 1, "file_nam": [1, 2, 5], "domain_writing_": [1, 2], "spot": 1, "number": [1, 2, 5], "num_x": [1, 2], "8": [1, 2, 5], "num_i": [1, 2], "count_img": 1, "64": [1, 5], "variabl": 1, "how": [1, 5], "mani": 1, "imag": [1, 2, 5], "have": [1, 5], "pixel": [1, 5], "chang": 1, "work": 1, "chdir": [1, 2], "creat": 1, "arrai": [1, 5], "amplitud": [1, 5], "zero": [1, 5], "phase": [1, 5], "frequenc": [1, 5], "qfactor": 1, "topographi": 1, "i": [1, 2, 5], "rang": [1, 2, 4, 5], "h5": [1, 5], "_0": 1, "hf5": [1, 5], "format": [1, 2], "be_qf": 1, "BE": 1, "quick": [1, 5], "fit": [1, 5], "be_ch": 1, "channel": [1, 2, 5], "0": [1, 2, 5], "3": [1, 5], "1": [1, 5], "2": [1, 5], "nor_amplitud": 1, "min": 1, "ptp": 1, "nor_phas": 1, "nor_frequ": 1, "nor_topographi": 1, "result": [1, 3], "fig": 1, "ax": [1, 5], "subplot": [1, 2, 5], "4": [1, 5], "figsiz": [1, 2, 5], "16": [1, 2], "dpi": [1, 2, 5], "100": [1, 2, 5], "subplots_adjust": [1, 5], "left": [1, 2, 5], "02": [1, 2, 5], "bottom": [1, 2, 5], "06": 1, "right": [1, 2, 5], "95": 1, "top": [1, 2, 5], "99": 1, "wspace": [1, 5], "25": [1, 5], "cm": 1, "viridi": 1, "shrink": 1, "6": [1, 2], "im0": 1, "imshow": [1, 2, 5], "1000": 1, "origin": 1, "lower": 1, "interpol": 1, "nearest": 1, "cmap": 1, "colorbar": 1, "label": 1, "u": [1, 5], "axi": [1, 2, 5], "off": [1, 5], "im1": 1, "rad": [1, 5], "im2": 1, "khz": 1, "im3": 1, "vmin": 1, "vmax": 1, "250": 1, "q": 1, "factor": 1, "show": [1, 2, 5], "specif": [1, 2], "togeth": 1, "subplot_kw": 1, "xtick": 1, "ytick": 1, "gridspec_kw": 1, "dict": 1, "hspace": 1, "zip": 1, "flat": 1, "ar": [1, 2, 4, 5], "now": [1, 5], "can": [1, 2, 5], "etc": [1, 2, 5], "win32com": [2, 5], "client": [2, 5], "time": [2, 3, 5], "pynsid": [2, 5], "from": [2, 3, 5], "tqdm": [2, 5], "acquit": [2, 5], "py": [2, 5], "acquisition_v0_9": [2, 5], "acquisit": [2, 5], "includ": [2, 5], "acquistion_v": [2, 5], "same": [2, 5], "ext": 2, "version": [2, 5], "pyscann": [2, 5], "also": [2, 5], "newexp": [2, 5], "exe_path": [2, 5], "bepyae_labview": [2, 5], "060523": [2, 5], "01": [2, 5], "offlin": [2, 5], "develop": [2, 3, 4, 5], "build": [2, 5], "connect": [2, 5], "between": [2, 5], "get": [2, 5], "init_bepya": [2, 5], "offline_develop": [2, 5], "true": [2, 5], "execut": [2, 4, 5], "initl": [2, 5], "hereinaft": 2, "If": [2, 5], "provid": [2, 5], "function": [2, 4], "util": [2, 4, 5], "default": [2, 5], "within": [2, 4, 5], "certain": 2, "feedback": [2, 5], "after": [2, 5], "which": [2, 5], "disabl": 2, "feedbackon": [2, 5], "fals": [2, 5], "allow": [2, 3, 5], "deactiv": 2, "dure": [2, 5], "iter": [2, 3, 5], "instanc": 2, "when": [2, 5], "requir": [2, 3], "note": [2, 5], "For": [2, 5], "correspond": 2, "hand": 2, "side": [2, 5], "x": [2, 5], "y": [2, 5], "while": [2, 5], "setpoint": [2, 5], "tip_control": [2, 5], "tip_parms_dict": [2, 5], "set_point_v_00": [2, 5], "next_x_pos_00": [2, 5], "5": [2, 5], "next_y_pos_01": [2, 5], "do_move_tip": [2, 5], "do_set_setpoint": [2, 5], "code": [2, 5], "v": [2, 5], "move": [2, 5], "afm": [2, 5], "platform": [2, 5], "amplifi": [2, 5], "type": [2, 5], "define_io_clust": [2, 5], "io_cluster_parms_dict": [2, 5], "analog_output_amplifier_06": [2, 5], "channel_01_type_07": [2, 5], "channel_02_type_08": [2, 5], "channel_03_type_09": [2, 5], "cypher": [2, 5], "6124": [2, 5], "4000000": [2, 5], "10": [2, 5], "ac": [2, 5], "dc": [2, 5], "ao0": [2, 5], "none": [2, 5], "extern": [2, 5], "define_be_parm": [2, 5], "be_parms_dict": [2, 5], "center_frequency_hz_00": [2, 5], "335": [2, 5], "band_width_hz_01": [2, 5], "amplitude_v_02": [2, 5], "phase_variation_03": [2, 5], "repeats_04": [2, 5], "req_pulse_duration_s_05": [2, 5], "auto_smooth_ring_06": [2, 5], "do_create_be_waveform": [2, 5], "335000": [2, 5], "100000": [2, 5], "004": [2, 5], "3352": [2, 5], "2952763920002": [2, 5], "12159459061880915": [2, 5], "singl": [2, 5], "return": [2, 5], "dataset": [2, 5], "quick_fit": [2, 5], "complex": [2, 3, 5], "spectra": [2, 5], "qk_fit": [2, 5], "com_spec": [2, 5], "chn1": [2, 5], "chn2": [2, 5], "chn3": [2, 5], "do_line_scan": [2, 5], "line_scan_parms_dict": [2, 5], "num_be_pulses_01": [2, 5], "32": [2, 5], "start_x_pos_00": [2, 5], "start_y_pos_01": [2, 5], "stop_x_pos_02": [2, 5], "stop_y_pos_03": [2, 5], "upload_to_daq": [2, 5], "voltag": [2, 5], "offset": [2, 5], "end": [2, 5], "posit": [2, 5], "done": [2, 5], "In": [2, 3, 5], "begin": 2, "appli": 2, "switch": 2, "ferroelectr": [2, 5], "polar": [2, 5], "subsequ": 2, "bia": 2, "enhanc": 2, "piezorespons": [2, 5], "forc": [2, 5], "microscopi": [2, 4, 5], "conduct": 2, "structur": 2, "To": 2, "process": 2, "first": [2, 5], "determin": 2, "individu": 2, "There": 2, "two": 2, "scenario": 2, "consid": 2, "chosen": 2, "record": 2, "all": [2, 5], "demonstr": 2, "below": [2, 5], "altern": [2, 5], "case": 2, "shown": [2, 5], "magnitud": 2, "A": 2, "length": 2, "t": 2, "again": [2, 5], "The": [2, 5], "e": [2, 5], "g": [2, 5], "valu": [2, 5], "uniformli": 2, "distribut": 2, "specifi": [2, 5], "custom": [2, 5], "suit": 2, "experiment": [2, 3], "typic": 2, "uniform": 2, "across": 2, "principl": 2, "span": 2, "start_point_x": 2, "end_point_x": 2, "direct": 2, "start_point_i": 2, "end_point_i": 2, "row": 2, "column": 2, "9": 2, "pos_x": 2, "linspac": 2, "pos_i": 2, "pulse_po": 2, "meshgrid": 2, "pulse_pos_x": 2, "reshap": 2, "pulse_pos_i": 2, "coordin": [2, 5], "size": [2, 5], "img_siz": 2, "check": [2, 5], "ab": 2, "print": [2, 5], "alert": 2, "overlap": 2, "along": 2, "elif": 2, "els": 2, "readi": 2, "len": [2, 5], "min_voltag": 2, "max_voltag": 2, "vdc_amp": 2, "min_time_log": 2, "max_time_log": 2, "vdc_time": 2, "dtype": [2, 5], "float32": 2, "power": [2, 3], "vdc": 2, "error": [2, 5], "No": 2, "enough": 2, "condit": 2, "expier": 2, "vdc_list": 2, "npy": 2, "asarrai": [2, 5], "sleep": [2, 5], "v_amp": 2, "v_time": 2, "define_apply_puls": [2, 5], "pulse_parms_dict": [2, 5], "pulse_init_amplitude_v_00": [2, 5], "pulse_mid_amplitude_v_01": [2, 5], "pulse_final_amplitude_v_02": [2, 5], "pulse_on_duration_s_03": [2, 5], "rise_time_s_05": [2, 5], "1e": [2, 5], "pulse_final_duration_s_04": [2, 5], "20e": [2, 5], "pulse_repeats_06": [2, 5], "do_create_puls": [2, 5], "do_upload_puls": [2, 5], "do_apply_puls": [2, 5], "dset_pfm": [2, 5], "dset_chn": [2, 5], "dset_c": [2, 5], "raster_scan": [2, 5], "raster_parms_dict": [2, 5], "scan_pixel": [2, 5], "scan_x_start": [2, 5], "scan_y_start": [2, 5], "scan_x_stop": [2, 5], "scan_y_stop": [2, 5], "progress_on": [2, 5], "ploton": [2, 5], "plot": [2, 5], "f": [2, 5], "ax1": [2, 5], "ax2": [2, 5], "ax3": [2, 5], "ax4": [2, 5], "ax5": 2, "ax6": 2, "30": 2, "00": [2, 5], "s": [2, 5], "appdata": [2, 5], "local": [2, 5], "anaconda3": [2, 5], "lib": [2, 5], "site": [2, 5], "packag": [2, 3, 4, 5], "hdf_util": [2, 5], "376": [2, 5], "futurewarn": [2, 5], "validate_h5_dimens": [2, 5], "remov": [2, 5], "futur": [2, 3, 5], "warn": [2, 5], "pfm_whole": 2, "progress": 2, "35": 2, "eta": [2, 5], "list": 2, "add": 2, "append": 2, "39": [2, 5], "04": 2, "42": 2, "22": 2, "08": 2, "38": 2, "05": 2, "45": 2, "54": 2, "46": 2, "33": 2, "88": 2, "19": 2, "55": 2, "50": 2, "34": 2, "90": 2, "indexerror": 2, "traceback": [2, 5], "most": [2, 5], "recent": [2, 5], "call": [2, 5], "last": [2, 5], "cell": [2, 5], "11": 2, "7": [2, 5], "12": 2, "13": 2, "14": 2, "17": 2, "index": [2, 5], "out": 2, "bound": 2, "object": [3, 5], "cut": 3, "edg": 3, "python": [3, 4, 5], "integr": 3, "our": [3, 4, 5], "self": [3, 5], "applic": 3, "program": [3, 4, 5], "interfac": 3, "api": [3, 5], "bepya": [3, 4], "aim": 3, "revolution": [3, 4, 5], "measur": [3, 5], "enabl": [3, 4, 5], "easi": 3, "implement": 3, "formul": 3, "orchestr": 3, "design": [3, 5], "gather": 3, "data": [3, 5], "more": 3, "effici": 3, "addit": [3, 5], "machin": 3, "leanr": 3, "model": 3, "oper": [3, 4, 5], "har": [3, 4, 5], "ai": 3, "real": 3, "analysi": 3, "decis": 3, "make": [3, 5], "rapid": 3, "larg": 3, "acceler": 3, "scientif": 3, "discoveri": 3, "With": 3, "capabl": [3, 4, 5], "activ": 3, "learn": 3, "fly": 3, "adapt": 3, "optim": 3, "paramet": 3, "drive": [3, 5], "becom": 3, "realiti": 3, "discov": 3, "potenti": [3, 4, 5], "welcom": [4, 5], "comprehens": [4, 5], "guid": 4, "scan": 4, "probe": [4, 5], "spm": [4, 5], "decdic": [4, 5], "incorpor": [4, 5], "wide": [4, 5], "command": 4, "facilit": [4, 5], "basic": [4, 5], "microscop": [4, 5], "ex": 4, "perform": [4, 5], "task": [4, 5], "eas": [4, 5], "essenti": 4, "avail": [4, 5], "explor": [4, 5], "syntax": [4, 5], "usag": [4, 5], "empow": [4, 5], "full": [4, 5], "system": [4, 5], "whether": [4, 5], "season": [4, 5], "new": [4, 5], "world": [4, 5], "experienc": [4, 5], "societi": [4, 5], "serv": [4, 5], "foundat": [4, 5], "your": [4, 5], "journei": [4, 5], "excit": [4, 5], "realm": [4, 5], "control": 4, "By": [4, 5], "gain": [4, 5], "abil": [4, 5], "write": [4, 5], "wai": [4, 5], "thing": 5, "necessari": 5, "directori": 5, "Then": 5, "otherwis": 5, "run": 5, "init": 5, "_bepya": 5, "input": 5, "take": 5, "some": 5, "turn": 5, "handsid": 5, "us": 5, "_control": 5, "exampl": 5, "locaiton": 5, "order": 5, "correct": 5, "hardwar": 5, "compon": 5, "involv": 5, "thu": 5, "inform": 5, "defin": 5, "_io": 5, "_cluster": 5, "bepfm": 5, "One": 5, "popular": 5, "band": 5, "_be": 5, "_parm": 5, "_line": 5, "_scan": 5, "stop": 5, "fucntion": 5, "just": 5, "squar": 5, "_pixel": 5, "region": 5, "point": 5, "save": 5, "name": 5, "_name": 5, "test": 5, "see": 5, "manual": 5, "ha": 5, "typeerror": 5, "over": 5, "vari": 5, "should": 5, "an": 5, "empti": 5, "keyboardinterrupt": 5, "aecroscopy_loc": 5, "python_guid": 5, "668": 5, "665": 5, "bar_progress": 5, "progress_bar": 5, "int": 5, "raster_parms_list": 5, "666": 5, "667": 5, "strat": 5, "po": 5, "669": 5, "scan_line_arrai": 5, "670": 5, "transit_time_s_02": 5, "671": 5, "wait": 5, "until": 5, "672": 5, "getcontrolvalu": 5, "move_tip_control_clust": 5, "300": 5, "298": 5, "299": 5, "action": 5, "302": 5, "303": 5, "304": 5, "visual": 5, "inlcud": 5, "20": 5, "image_stack": 5, "dask": 5, "shape": 5, "float64": 5, "chunksiz": 5, "chunktyp": 5, "ndarrai": 5, "contain": 5, "pfm": 5, "gener": 5, "dimens": 5, "m": 5, "respons": 5, "axesimag": 5, "0x1ba0b485a50": 5, "d": 5, "0x1ba0b4448e0": 5, "chunk": 5, "byte": 5, "97": 5, "mib": 5, "62": 5, "count": 5, "complex128": 5, "load": 5, "analyz": 5, "hf": 5, "test_0": 5, "hdf": 5, "print_tre": 5, "0x1ba0c06efb0": 5, "piezoresponc": 5, "spectroscopi": 5, "_bep": 5, "_xxx": 5, "howev": 5, "_paramet": 5, "wavefrom": 5, "step": 5, "cycl": 5, "define_beps_paramet": 5, "beps_parms_dict": 5, "amplitude_v_00": 5, "offset_v_01": 5, "read_voltage_v_02": 5, "step_per_cycle_03": 5, "num_cycles_04": 5, "cycle_fraction_05": 5, "cycle_phase_shift_06": 5, "measure_loops_07": 5, "transition_time_s_08": 5, "delay_after_step_s_09": 5, "do_create_waveform": 5, "001": 5, "_grid": 5, "_dict": 5, "beps_waveform": 5, "beps_quick_fit": 5, "beps_cx": 5, "beps_chn": 5, "do_beps_grid": 5, "beps_grid_parms_dict": 5, "pixel_num_x": 5, "pixel_num_i": 5, "beps_grid": 5, "waveform": 5, "set_ylabel": 5, "set_xlabel": 5, "text": 5, "dru": 5, "loop": 5, "convert": 5, "seper": 5, "field": 5, "on_field_quick_fit": 5, "off_field_quick_fit": 5, "idx": 5, "18": 5, "set_titl": 5, "vs": 5, "On": 5, "_specif": 5, "do_beps_specif": 5, "beps_at_specific_loc": 5, "want": 5, "featur": 5, "observ": 5, "often": 5, "coordiant": 5, "_coordin": 5, "130": 5, "converted_coor": 5, "convert_coordin": 5, "original_coordin": 5, "num_pix_x": 5, "256": 5, "num_pix_i": 5, "21875": 5, "015625": 5, "character": 5, "manipul": 5, "via": 5, "film": 5, "flip": 5, "_appli": 5, "_puls": 5, "durat": 5, "10e": 5, "suptitl": 5, "autom": 5, "autonom": 5, "so": 5, "_bar": 5, "assist": 5, "track": 5, "max_valu": 5, "do_vs_waveform": 5, "updat": 5, "variou": 5, "option": 5, "trajectori": 5, "equip": 5, "sprial": 5, "ani": 5, "_spiral": 5, "inner": 5, "radiu": 5, "outer": 5, "sprial_result": 5, "fpga_spiral_scan": 5, "spiral_parms_dict": 5, "spiral_inner_radius_x_v_00": 5, "spiral_outer_radius_x_v_01": 5, "spiral_inner_radius_y_v_02": 5, "spiral_outer_radius_y_v_03": 5, "spiral_n_cycles_04": 5, "spiral_duration_05": 5, "spiral_dose_distribution_06": 5, "spiral_direction_07": 5, "spiral_return_opt_08": 5, "scan_x_offset_v": 5, "scan_y_offset_v": 5, "scan_rotation_deg": 5, "do_scan_upd": 5, "do_scan": 5, "spiral_scan": 5, "either": 5, "beforehand": 5, "fpga_result": 5, "be_result": 5, "fpga_spiral_scan_b": 5, "num_be_puls": 5, "128": 5, "do_be_arb_line_update_00": 5, "do_be_arb_line_scan_01": 5, "spiral_reconstruct": 5, "_tip": 5, "fpga_tip_control": 5, "fpga_tip_parms_dict": 5, "strat_x_position_v_00": 5, "strat_y_position_v_01": 5, "final_x_position_v_02": 5, "final_y_position_v_03": 5, "make_cur_pos_start_po": 5, "do_probe_move_upd": 5, "do_probe_mov": 5, "current": 5, "_cur": 5, "_po": 5, "_start": 5, "final": 5, "_linebylin": 5, "_raster": 5, "slow": 5, "_full": 5, "_to": 5, "_advanc": 5, "_next": 5, "_onli": 5, "raster_ful": 5, "fpga_linebyline_raster_scan": 5, "line_by_line_raster_dict": 5, "raster_scan_size_x_v_00": 5, "raster_scan_size_y_v_01": 5, "raster_n_scan_lines_02": 5, "raster_line_duration_s_03": 5, "scan_x_offset_v_04": 5, "scan_y_offset_v_05": 5, "scan_rotation_deg_06": 5, "initialize_line_by_line_rast": 5, "do_full_raster_scan": 5, "wait_to_advance_to_next_lin": 5, "do_next_raster_line_onli": 5, "stop_full_raster_scan": 5, "raster_lin": 5}, "objects": {}, "objtypes": {}, "objnames": {}, "titleterms": {"high": [0, 1, 2], "throughput": [0, 1, 2], "experiment": 0, "notebook": 1, "domain": [1, 2], "write": [1, 2], "analysi": 1, "import": [1, 2, 5], "set": [1, 2, 5], "directori": [1, 2], "root": 1, "name": 1, "your": 1, "dataset": 1, "load": 1, "all": 1, "data": [1, 2], "plot": 1, "workflow": 2, "instal": [2, 5], "start": [2, 5], "bepya": [2, 5], "ex": [2, 5], "vi": [2, 5], "initi": [2, 5], "igor": [2, 5], "ar18": [2, 5], "tip": [2, 5], "paramet": [2, 5], "io": [2, 5], "BE": [2, 5], "puls": [2, 5], "run": 2, "line": [2, 5], "scan": [2, 5], "test": 2, "experi": 2, "1": 2, "perform": 2, "each": 2, "measur": 2, "new": 2, "locat": [2, 5], "pre": 2, "defin": 2, "prior": 2, "expeir": 2, "save": 2, "step": 2, "gener": 2, "arrai": 2, "2": 2, "establish": 2, "3": 2, "4": 2, "do": [2, 5], "bepfm": 2, "whole": 2, "area": 2, "random": 2, "space": 2, "welcom": 3, "aecroscopi": [3, 4, 5], "autom": 3, "autonom": 3, "microscopi": 3, "introduct": 4, "guid": 5, "essenti": 5, "command": 5, "function": 5, "hereinaft": 5, "raster": 5, "result": 5, "bep": 5, "grid": 5, "specif": 5, "appli": 5, "progress": 5, "bar": 5, "spiral": 5, "control": 5, "fpga": 5, "driven": 5}, "envversion": {"sphinx.domains.c": 2, "sphinx.domains.changeset": 1, "sphinx.domains.citation": 1, "sphinx.domains.cpp": 6, "sphinx.domains.index": 1, "sphinx.domains.javascript": 2, "sphinx.domains.math": 2, "sphinx.domains.python": 3, "sphinx.domains.rst": 2, "sphinx.domains.std": 2, "sphinx.ext.intersphinx": 1, "sphinx": 56}})