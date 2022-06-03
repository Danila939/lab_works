#include <iostream>
#include <thread>
#include <Windows.h>

#include <stack>

using namespace std;


HANDLE hSemaphore;

class ThreadSafeStack 
{
private:
    stack<int> stack;

public:
    void push(int elem, int ID)
    {
        WaitForSingleObject(hSemaphore, INFINITE);
        stack.push(elem);
        cout << "P " << ID << " -> " << elem << "\n";
        ReleaseSemaphore(hSemaphore, 1, nullptr);
    
    }

    bool try_pop(int &elem, int ID)
    {
        bool result = false;
        WaitForSingleObject(hSemaphore, INFINITE);
        if (!stack.empty())
        {
            result = true;
            elem = stack.top();
            stack.pop();
            cout << "C " << ID << " -> " << elem << "\n";
        }
        else
            cout << "C " << ID << " sleep\n";
        ReleaseSemaphore(hSemaphore, 1, nullptr);
        return result;

    }

};

ThreadSafeStack TSS;

void task_producer(int ID, long &WorkVolumeP)
{

    while (WorkVolumeP-- > 0)
    {
        int elem = rand() % 100;
        //this_thread::sleep_for(chrono::milliseconds(2));
        TSS.push(elem + ID, ID);
    }
}

void task_consumer(int ID, long &WorkVolumeC)
{

    while (_InterlockedDecrement(&WorkVolumeC) >= 0)
    {
        int elem;
        if (TSS.try_pop(elem, ID))
        {
            this_thread::sleep_for(chrono::milliseconds(5));
        }
        else 
            InterlockedIncrement(&WorkVolumeC);
    }
}



        //while (_InterlockedExchange(&ResourseInUse, true))
         //   Sleep(0);

        //while (_InterlockedCompareExchange(&lock, 1, 0) == 1)
          //  Sleep(0);

       // while (lock.exchange(true))
         //  Sleep(0);

        //while (flag.test_and_set())
          //  Sleep(0);


        //EnterCriticalSection(&cs);

       
        
        
        //LeaveCriticalSection(&cs);

       // _InterlockedCompareExchange(&lock, 0, 1);
        //_InterlockedExchange(&ResourseInUse, false)
        //lock.store(false);
        //flag.clear();
 

int main()
{

    long WorkVolumeP = 8;
    long WorkVolumeC = 8;
    srand(GetTickCount());
    hSemaphore = CreateSemaphore(nullptr, 1, 1, nullptr);

    thread worker[5];
    for (int i = 0; i < 5; i++)
    {
        if (i < 2)
            worker[i] = thread(task_producer, i, ref(WorkVolumeP));
        else
            worker[i] = thread(task_consumer, i, ref(WorkVolumeC));
    }
    //InitializeCriticalSection(&cs);

    for (int i = 0; i < 5; i++)
    {
        worker[i].join();
    }

    CloseHandle(hSemaphore);
    //DeleteCriticalSection(&cs);
    cin.get();
    return 0;
}


