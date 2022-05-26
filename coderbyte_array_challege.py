'''
My solution for Coderbyte ArrayChallege
'''

list = ["10:10AM-10:20AM","12:05PM-12:07PM","12:15PM-02:00PM","09:00AM-10:00AM","11:30AM-12:00PM","09:15PM-09:20PM","09:05PM-09:07PM","09:01PM-09:02PM"]
#list_am.extend(list_pm)

def check_free_time(list):
    # Sort by time
    to_hour_military = lambda num : 12 if (num==12) else num+12
    list_am = sorted([e for e in list if e.split("-")[0][-2:].lower() == "am"], key=lambda ev: int(ev.split("-")[0][:2]*60)+int(ev.split("-")[0][3:5]))
    list_pm = sorted([e for e in list if e.split("-")[0][-2:].lower() == "pm"], key=lambda ev: (to_hour_military(int(ev.split("-")[0][:2])),int(ev.split("-")[0][3:5])))
    
    # Time AM
    final_time_am = 0
    last_time_am = 0
    if list_am:
        for ev in list_am:
            event = ev.split("-")
            mins_start = (int(event[0][:2])*60)+int(event[0][3:5])
            mins_end = (int(event[1][:2])*60)+int(event[1][3:5])
            if list_am.index(ev) == 0:
                last_time_am = mins_end
                continue
            ev_free_time = abs((last_time_am - mins_start))
            if final_time_am < ev_free_time: 
                final_time_am = ev_free_time   
            #final_time_am = abs((last_time_am - mins_start))    
            last_time_am = mins_end

    if list_pm:
        # Time PM
        final_time_pm = 0
        last_time_pm = []    
        for ev in list_pm:
            event = ev.split("-")
            hour_start = int(event[0][:2])
            mins_start = int(event[0][3:5])
            hour_end = int(event[1][:2])
            mins_end = int(event[1][3:5])
            
            if list_pm.index(ev) == 0:
                last_time_pm = [hour_end,mins_end]
                continue
            
            ev_free_time = ((to_hour_military(hour_start) - to_hour_military(last_time_pm[0]))*60)+(mins_start-last_time_pm[1])
            if final_time_pm < ev_free_time:
                final_time_pm = ev_free_time
            last_time_pm = [hour_end,mins_end]
    
    print(list_am+list_pm,"\n")
    if final_time_am > final_time_pm:
        hour = int(final_time_am/60)
        min = final_time_am - hour * 60
        if len(str(hour)) == 1 : hour = "0"+str(hour)
        if len(str(min)) == 1 : min = "0"+str(min)
        return print(hour,":",min,sep="")
    
    hour = int(final_time_pm/60)
    min = final_time_pm - hour * 60
    if len(str(hour)) == 1 : hour = "0"+str(hour)
    if len(str(min)) == 1 : min = "0"+str(min)
    return print(hour,":",min,sep="")

check_free_time(list)
    
    
