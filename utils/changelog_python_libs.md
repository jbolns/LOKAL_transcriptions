# Modifications to underlying libraries
LOKAL aims to deliver existing open-source resources, rather than re-invent them. If small changes to underlying libraries are needed for any reason, they should be declared here.


## rich

### File: rich/progress.py

#### Lines 1446 - 1449.
* Added.
* Reason: Ugly hack, but it prints updates to GUI.
```
# START of EDIT for use w. LOKAL – ugliest hack ever, but it prints updates to GUI.
if task.completed/task.total > 0 and task.completed/task.total < 1:
    print(task.description + int(task.completed/task.total*20) * '━', int(task.completed/task.total*100), '%')
# END of EDIT for use w. LOKAL
```

## tqdm
### File: tqdm/std.py

#### Line 628.
* Modified
* Reason: Forces some consistency between whisper and faster-whisper progress bars.
```
bar_format = '{l_bar}{bar:20}{r_bar}\n'  # EDIT for use w. LOKAL – to force some consistency between whisper and faster-whisper progress bars.
```
