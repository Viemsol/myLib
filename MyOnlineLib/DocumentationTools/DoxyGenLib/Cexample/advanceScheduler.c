

/**
*
*\mainpage Description
* nnnnnnnnnnnnnnf
* fffffffffff
* hhhhhhhhhhhhhh
*\section Chapeter1
*\subsection  Topic1
*nnnnnnnnnnnnnnn
*\subsection Topic2
*kkkkkkkkkkkkkkkkkk
*\section Chapeter2
* chapter description
*\subsection Topic3
* lllllllllllllllllllllll
*/


/**
*@file advanceScheduler.c
*@author Nandkumar Ganesh Dhavalikar
*@date 10-2-2019
*@brief  Simple Sigle Page scheduler
* example of siple Scheduler for embeeded system
* Events can be pushed from ISR or from application
* Timer Events
* Expandable timers and Event Buffers
* sleep condition check
*
*/

/**
*@brief Syste event
*Differant sys events
*/

enum sysEvents
{
    MAXEVENT    = 8,         /**< MAX event can be stored in ring buffer*/
    MAXSTIMER   = 4,         /**< MAX one Sec resolution timers */
    MAXMSTIMER  = 4,         /**< MAX ten milli sec resolution timers */ 
};                                                      

/**
*@brief Function Put next event
*next description
*<b> bold description </b>
*@code
*void putNextEvent(void * fptr, void * data)
*@endcode
*@param fptr function pointer
*@param data data pointer
*@return true or flase
*@note call this function in ISR and if outside ISR with critical section
*@note This is function note
*@warning This is function Warning
*/

bool  putNextEvent(void * fptr, void * data)
{
    static bool stOverflow = false;
    DISABLE_GLOBAL_ISR
    if(!stOverflow)
    {
        strScheduler.fptr[strScheduler.eventH] = fptr;
        strScheduler.data[strScheduler.eventH] = data;
        strScheduler.eventH++;
        if(strScheduler.eventH >= MAXEVENT)
        {
           strScheduler.eventH = 0; 
        }
    }
    if(strScheduler.eventT == strScheduler.eventH)
    {
        stOverflow = true;
        printf("Possible Overflow on next push, so discard new events\n");
    }
    else
    {
        stOverflow = false;
    }
    ENABLE_GLOBAL_ISR
    return true;
}