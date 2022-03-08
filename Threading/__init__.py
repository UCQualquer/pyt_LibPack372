from threading import Event, Thread as __Thread
from typing import Callable, Dict, Tuple, Union
from My_Pack.Essentials import ensureType
import sys, inspect

class NotStartedException(Exception):
    pass

class Thread(__Thread):
    def __init__(self, target: Callable, args: Tuple = (), custom_data: dict = {}, **kwargs):
        ensureType(args, tuple, 'args')
        ensureType(custom_data, dict, 'custom_data')
        
        super().__init__(target = target, args = args, **kwargs)

        self.Start = self.start # Backwards compat
        self.Join = self.join # Backwards compat

        # [True] if thread is still running, else [False].
        # Read only.
        self.running_: Event = Event() # https://docs.python.org/3/library/threading.html#event-objects

        # [True] if thread has completed its work, else [False].
        # Read only.
        self.complete_: Event = Event() # https://docs.python.org/3/library/threading.html#event-objects

        # Custom data that will be provided on thread creation, and acessed after.
        # Read only. Not modified in any situation.
        # Use example:
        ## >>> th = Thread(target = ..., args = (...), custom_data = {'test': 123})
        ## >>> th.CustomData
        ## {'test': 123}
        self.__custom_data: dict = custom_data
    

    # See [Thread.running_]
    @property
    def IsRunning(self) -> bool:
        return self.running_.is_set()
    
    # See [Thread.complete_]
    @property
    def IsComplete(self) -> bool:
        return self.complete_.is_set()
    
    # See [Thread.__custom_data]
    @property
    def CustomData(self):
        return self.__custom_data

    def start(self):
        """
            Starts the thread. Will not join it.

            If not joined, [Thread.IsRunning] and [Thread.IsComplete] will be set up to [False] and [True] forever.
            Use [Threading] to avoid it, as it will create another thread to join, not blocking the system and allowing the variables to change.
        """
        try:
            super().start()
            self.complete_.clear()
            self.running_.set()

        except (KeyboardInterrupt, SystemExit):
            sys.exit()
        except Exception as ex:
            raise ex
    
    def join(self, timeout: Union[float, None] = None):
        """
            Will join previously started thread (use [Thread.Start]).

        Args:
            timeout (float | None, optional): Timeout of thread. Will kill it if thread's running time reach [timeout]. Defaults to None.
        """
        super().join(timeout = timeout)
        self.complete_.set()
        self.running_.clear()
    
    def startAndJoin(self, timeout: Union[float, None] = None):
        try:
            super().start()
            self.complete_.clear()
            self.running_.set()
            super().join(timeout = timeout)
            self.complete_.set()
            self.running_.clear()

        except (KeyboardInterrupt, SystemExit):
            sys.exit()
        except Exception as ex:
            self.complete_.clear()
            self.running_.clear()
            raise ex

class Threading(object):
    # Dict containing thread's id and it's object: {0: Thread(...), 1: Thread(...)}
    # Not intended to be modified outside.
    # Can be used to iterate over threads
    threads: Dict[int, Thread] # {thread_id: thread_obj}

    # Last id on [Threading.threads]. Defaults to [-1]
    # Not intended to be modified outside.
    lastId: int = -1

    # If thread target supports key-arguments, it will pass this [Threading] [self] object as kwargs['threading_obj']
    # and it own id as kwargs['thread_id']

    def __init__(self):
        self.threads = {}
        self.lastId = -1


    @property
    def ThreadCount(self) -> int:
        """
            Returns the threads count, running or not, completed or not.

        Returns:
            int: How many threads in [Threading.threads].
        """
        return len(self.threads)
    
    @property
    def RunningCount(self) -> int:
        """
            Returns the running threads count. Will no add up completed or not started threads.

        Returns:
            int: How many running threads in [Threading.threads].
        """
        
        i = [None for v in self.threads.values() if v.IsRunning and not v.IsComplete]
        return len(i)
    
    @property
    def CompleteCount(self) -> int:
        """
            Returns the complete threads count. Will no add up running or not started threads.

        Returns:
            int: How many completed threads in [Threading.threads].
        """

        i = [None for v in self.threads.values() if v.IsComplete and not v.IsRunning]
        return len(i)
    
    @property
    def AllComplete(self) -> bool:
        """
            Returns [True] if all threads in [Threading.threads] are complete.

        Returns:
            bool: [True] if all threads are complete, else [False].
        """

        return ((self.RunningCount == 0) and (self.ThreadCount == self.CompleteCount))

    def AddThread(self, target: Callable, args: Tuple = (), run: bool = False, custom_data: dict = {}, **kwargs) -> Tuple[int, Thread]:
        """
            Add thread to [Threading.threads].

        Args:
            target (Callable): Function to thread.
            args (Tuple): Function's parameters.
            run (bool, optional): [True] to start thread, else [False]. Defaults to [False].

        Returns:
            int: Created thread id.
            Thread: Created thread.
        """

        ensureType(args, tuple, 'args')
        ensureType(run, bool, 'run')

        self.lastId += 1
        thread_id = self.lastId

        kwargs['daemon'] = True
        if bool(inspect.getfullargspec(target)[2]):
            kwargs['kwargs'] = {'threading_obj': self, 'thread_id': thread_id, 'custom_data': custom_data}

        t = Thread(target, args, custom_data, **kwargs)
        self.threads[thread_id] = t
        if run:
            self.StartThread(thread_id)

        return (thread_id, t)
    
    def JoinThread(self, thread_id: int):
        ensureType(thread_id, int, 'thread_id')

        thr = self.threads[thread_id]
        if thr.IsRunning:
            thr.join()

        elif not thr.IsComplete:
            thr.running_.wait()
            thr.join()
        
        else:
            raise NotStartedException

    def StartThread(self, thread_id: int):
        """
            Starts thread [Threading.threads[thread_id]].

        Args:
            thread_id (int): Thread id, which is the key in [Threading.threads].
        """

        ensureType(thread_id, int, 'thread_id')

        thr = self.threads[thread_id]
        if not thr.IsComplete and not thr.IsRunning:
            self.__followThread(thread_id)
        else:
            raise NotStartedException

    def StartAll(self):
        """
            Starts all threads that are in [Threading.threads].
            
            See [Threading.StartThread] for details
        """
        for thread_id in self.threads.keys():
            self.StartThread(thread_id)
    
    def DeleteThread(self, thread_id: int, force: bool = False):
        """
            Deletes thread from [Threading.threads]. Will not stop thread.

        Args:
            thread_id (int): Thread id in [Threading.threads] to be deleted.
            force (bool, optional): [True] if should kill thread if it stills running, else [False]. Defaults to False.

        Raises:
            ValueError: Raises if said thread does not exist.
            ValueError: Raises if said thread is still running. Use [force = True].
        """

        ensureType(thread_id, int, 'thread_id')
        ensureType(force, bool, 'force')

        if thread_id not in self.threads.keys():
            raise ValueError(f'Thread id [{thread_id}] does not exist')
        
        value = self.threads[thread_id]

        if value.IsRunning and not value.IsComplete and force == False:
            raise ValueError(f'Thread id [{thread_id}] is still running. Call function with [force = True] to ignore this protection.')
        
        else:
            del self.threads[thread_id]
    
    def __followThread(self, thread_id: int):
        """
            Will create a thread to follow another thread. Ironic, no?

        Raises:
            ValueError: Raises if thread does not exist.
        """
        ensureType(thread_id, int, 'thread_id')

        if thread_id not in self.threads.keys():
            raise ValueError(f'Thread id [{thread_id}] does not exist')

        try:
            # It starts a new thread because it needs the [.Join] to occur, but if it happens outside a thread, it would lock the system.
            # And it needs to join because [Thread.IsRunning] and [Thread.IsComplete] to be set up.
            
            thread_obj = self.threads[thread_id]
            def t():
                thread_obj.startAndJoin()
            
            # No, it won't create a loop. The loop would occur if it started through Threading,
            # but it starts directly in the thread obj.
            #
            # Again, the thread state follow would only occur if it was started in [Threading.Start],
            # but it starts in [THREAD.Start]...

            #Thread(t, daemon = True).Start()
            Thread(t, daemon = True).start()

        except Exception as ex:
            raise ex




