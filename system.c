#include <sys/wait.h>
#include <errno.h>
#include <unistd.h>

int system(const char* cmdString)
{
    pid_t pid;
    int status;

    if (cmdString == NULL) {
        return 1; 
    }

    if ((pid = fork()) < 0) {
        status = -1; 
    } else if (pid == 0) {
        execl("/bin/bash", "bash", "-c", cmdString, (char*)0);
        _exit(127);
    } else {
        while (waitpid(pid, &status, 0)) {
            if (errno != EINTR) {
                status = -1; 
                break;
            } 
        }
    }

    return status;
}

int main(void)
{
    system("python test.py");

    return 0;
}
