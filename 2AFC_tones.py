from psychopy import visual, event, gui, core, sound
import glob # glob is module that has a function that retrieves files (e.g., of images) from a directory
import pandas as pd # pandas is a module that allows to create data-frames
import module_waveforms as wf
import sounddevice as sd
import random

win = visual.Window(color="white",fullscr=False)

## helper functions 
# function to display text
def text_fx(curtxt,colx):
	curtxt = visual.TextStim(win,text=curtxt,color=colx)
	if(curtxt!=0):
		curtxt.draw()
	win.flip()
# function to generate a given trial's comparison stimulus
def update_compStim(hz_compStim,cur_amp):
		compStim = {
			"type": "comparison",
			"hz": hz_compStim,
			"cur_amp": cur_amp,
			"waveform": wf.soundGene2(44100,1,hz_compStim,cur_amp)
		}
		return compStim

# define columns for dataframe
columns = ['id','stand_stim_hz','stand_stim_amp','comp_stim_hz','#trials',
'moli','cur_amp','nReverse']
# generate dataframe
data = pd.DataFrame(columns=columns)
## generate the standard stimulus (constant)
# freqs_catcim = [125, 129, 133, 137, 141, 145, 149]; mean = 137
standard_stim = {
	"type": "standard",
	"hz": 137,
	"cur_amp": .5,
	"waveform": wf.soundGene2(44100,1,137,.5)
}
# list of all comparison stimuli; Note: "moli" means "more or less intense"

list_compStims = [
	{"hz":125, "cur_amp":.5, "moli": "undefined", "nTrials":0, "nReverse":0},
	#{"hz":129, "cur_amp":.5, "moli": "undefined", "nTrials":0, "nReverse":0},
	#{"hz":133, "cur_amp":.5, "moli": "undefined", "nTrials":0, "nReverse":0},
	{"hz":137, "cur_amp":.5, "moli": "undefined", "nTrials":0, "nReverse":0},
	#{"hz":141, "cur_amp":.5, "moli": "undefined", "nTrials":0, "nReverse":0},
	#{"hz":145, "cur_amp":.5, "moli": "undefined", "nTrials":0, "nReverse":0},
	{"hz":149, "cur_amp":.5, "moli": "undefined", "nTrials":0, "nReverse":0}
]

nTrials_max = 1
nReverse_til_cia = 2
nReverse_til_stop = nReverse_til_cia*2

while True:
	# Go through list_compStims and check, if there are still ...
	# ... uncompleted comparison stimuli
	compStims_uncompleted_ind = []
	for stim_x in range(len(list_compStims)):
		if list_compStims[stim_x]["nReverse"] < nReverse_til_stop:
			compStims_uncompleted_ind.append(stim_x)
	# Randomly sample from compStims_uncompleted_ind
	if len(compStims_uncompleted_ind) != 0:
		indx_curStim = random.sample(compStims_uncompleted_ind,1)[0]
	else:
		break
	cur_compStim = list_compStims[indx_curStim]
	# update nTrials in list_compStims
	nTrials_prev = list_compStims[indx_curStim].get("nTrials")
	nTrials_now = {"nTrials": nTrials_prev + 1}
	list_compStims[indx_curStim].update(nTrials_now)
	# generate comparison stimulus' wave form (plus some information) for subsequent trial
	cur_compStim_wave = update_compStim(cur_compStim.get("hz"),cur_compStim.get("cur_amp"))
	cur_amp = cur_compStim.get("cur_amp")
	# make a list of the two alternatives for the 2AFC task
	trial_stims = [cur_compStim_wave,standard_stim]
	random.shuffle(trial_stims)

	## Show 'prepare' message
	text_fx("Press the key 'r' when you are ready for the next trial.","black")
	event.waitKeys(keyList=['r'])
	## Play the two waves, i.e., start trial
	for event_x in range(2):
		stimType = trial_stims[event_x].get("type")
		stim_nTrials = str(nTrials_now.get("nTrials"))
		stim_Hz = str(trial_stims[event_x].get("hz"))
		if event_x==0:
			stim_info = 'Stimulus #1 \n' + 'Type: ' + stimType ; colx="black"
		else:
			stim_info = 'Stimulus #2 \n' + 'Type: ' + stimType ; colx="blue"
		if stimType == "comparison": 
			stim_info = stim_info + "\n Hz: " + stim_Hz + "\n nTrials: " + stim_nTrials
		text_fx(stim_info,colx)
		core.wait(1) # wait one second
		stim_event_x = trial_stims[event_x].get("waveform")
		sd.play(stim_event_x,44100)
		sd.wait()

	## 2AFC
	text_fx("Which stimulus was more intense? \n"
		"Press 'f' if you think, it was the first one,"
		"\n press 'j', if you think, it was the second one.","black")
	keysToRecord = ['f','j']
	resp_key = event.waitKeys(keyList=keysToRecord)
	if resp_key[0] == keysToRecord[0]:
		firstOrSecond = 0 
	else:
		firstOrSecond = 1
	# Which type of stimulus appeared more intense?
	stimType_moreIntense = trial_stims[firstOrSecond].get("type")
	
	## Adjusting amplitude of comparison stimulus
	# Change in amplitude (cia) depends on nReverse
	nReverse_prev = list_compStims[indx_curStim].get("nReverse")
	cia = .1 if nReverse_prev < nReverse_til_cia else .05
	if stimType_moreIntense == "standard":
		cur_amp += cia
		moli_now = {"moli": "less"}
	else:
		cur_amp -= cia
		moli_now = {"moli": "more"}
	# update current_amplitude in list_comparison_stimuli
	amp_now = {"cur_amp": cur_amp}
	list_compStims[indx_curStim].update(amp_now)
	# update nReverse and then, the moli attribute
	moli_prev = list_compStims[indx_curStim].get("moli")
	nReverse_now = {"nReverse":0}
	if nTrials_now.get("nTrials") > 1:
		if moli_prev != moli_now.get("moli"):
			nReverse_now = {"nReverse": nReverse_prev + 1}
			list_compStims[indx_curStim].update(nReverse_now)
	list_compStims[indx_curStim].update(moli_now)
	

	# add trial data to dataframe
	data = data.append({
		'id': 'test',
		'stand_stim_hz': standard_stim.get("hz"),
		'stand_stim_amp': standard_stim.get("cur_amp"),
		'comp_stim_hz': cur_compStim_wave.get("hz"),
		'#trials': nTrials_now.get("nTrials"),
		'moli': moli_now.get("moli"),
		'cur_amp': cur_amp,
		'nReverse': nReverse_now.get("nReverse")
		}, ignore_index=True)

logfile_path = '/users/paulseitlinger/desktop/'
logfile_name = "{}logfile_{}.csv".format(logfile_path, 'test')
data.to_csv(logfile_name)

## Goodbye message
#text_fx("Thank you for your participation. Press any key to end the session.","white")
#event.waitKeys()


win.close






