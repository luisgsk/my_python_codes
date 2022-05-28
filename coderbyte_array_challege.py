'''
Have the function ArrayChallenge(strArr) read the strArr parameter being passed which will represent a full day 
and will be filled with events that span from time X to time Y in the day. The format of each event 
will be hh:mmAM/PM-hh:mmAM/PM. For example, strArr may be ["10:00AM-12:30PM”,"02:00PM-02:45PM”,"09:10AM-09:50AM”]. 

Your program will have to output the longest amount of free time available between the start of your first event 
and the end of your last event in the format: hh:mm. The start event should be the earliest event in the day and 
the latest event should be the latest event in the day. The output for the previous input would therefore be 01:30 
(with the earliest event in the day starting at 09:10AM and the latest event ending at 02:45PM). The input will contain 
at least 3 events and the events may be out of order.

Examples
Input: {"12:15PM-02:00PM”,"09:00AM-10:00AM”,"10:30AM-12:00PM”}
Output: 00:30
Input: {"12:15PM-02:00PM”,"09:00AM-12:11PM”,"02:02PM-04:00PM”}
Output: 00:04
'''

list = ["10:10AM-10:20AM","12:05PM-12:07PM","12:15PM-02:00PM","09:00AM-10:00AM","11:30AM-12:00PM","09:15PM-09:20PM","09:05PM-09:07PM","09:01PM-09:02PM"]
#list = ["10:00AM-12:30PM","02:00PM-02:45PM","09:10AM-09:50AM"]
#list = ["10:00AM-12:30PM","09:10AM-09:50AM"]
#list = ["02:00PM-02:45PM","03:45PM-04:00PM"]
#list = ["10:00AM-11:00AM","11:45AM-12:00PM"]

def check_free_time(list):
    if len(list) < 2:
        return print("Is not possible.")
    # Sort by time
    to_hour_military = lambda num : 12 if (num==12) else num+12
    list_am = sorted([e for e in list if e.split("-")[0][-2:].lower() == "am"], key=lambda ev: int(ev.split("-")[0][:2]*60)+int(ev.split("-")[0][3:5]))
    list_pm = sorted([e for e in list if e.split("-")[0][-2:].lower() == "pm"], key=lambda ev: (to_hour_military(int(ev.split("-")[0][:2])),int(ev.split("-")[0][3:5])))

    # Time AM
    final_time_am = 0
    last_time_am = 0
    if list_am != []:
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
            
    if list_pm != []:
        # Time PM
        final_time_pm = 0
        last_time_pm = []  
        for ev in list_pm:
            event = ev.split("-")
            hour_start = int(event[0][:2])
            mins_start = int(event[0][3:5])
            hour_end = int(event[1][:2])
            mins_end = int(event[1][3:5])
            
            if list_pm.index(ev) == 0 and list_am != []:
                ''' Se calcula la primera hora de inicio del primer evento PM con la ultima 
                    hora de termino de los eventos AM para sacar el tiempo libre entre estos
                    dos.
                    '''
                # Llevamos la ultima hora de eventos AM de minutos a hh mm
                h_last_time_am = int(last_time_am/60)
                m_last_time_am = last_time_am - h_last_time_am*60
                
                '''
                Aca a la hora de inicio del evento PM en formato de hora militar
                le restamos la cantidad de horas de la hora de termino del evento AM.
                
                Tambien al resultado de esto, lo transformamos de horas a minutos y le restamos
                el resultado de los minutos de la hora de inicio del evento PM menos los minutos
                de la hora de termino del evento Am.
                
                Con esto tenemos como resultado la cantidad de minutos de diferencia entre
                la ultima hora de termino del evento AM con la primera hora de inicio del
                evento PM (:
                '''
                h_diff_am_pm = to_hour_military(hour_start)-h_last_time_am
                m_diff_am_pm = abs(mins_start-m_last_time_am)
                final_time_pm = int(h_diff_am_pm*60)-m_diff_am_pm
                last_time_pm = [hour_end,mins_end]
                continue
            elif list_pm.index(ev) == 0:
                last_time_pm = [hour_end,mins_end]
                continue
            
            ev_free_time = ((to_hour_military(hour_start) - to_hour_military(last_time_pm[0]))*60)+(mins_start-last_time_pm[1])
            if final_time_pm < ev_free_time:
                final_time_pm = ev_free_time
            last_time_pm = [hour_end,mins_end]
    
    print("events:",list_am+list_pm,"\n")
    if (list_pm == []) or (final_time_am > final_time_pm):
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
    
    
