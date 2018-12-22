#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>

int main(int argc, char**argv)
{
	struct statx stx = { 0, };
	if (argc != 2) {
		printf("Usage: %s FILE\n", argv[0]);
		printf("Display btime of a given file in UNIX time format.\n");
		return EXIT_SUCCESS;
	}
	int rc = statx(AT_FDCWD, argv[1], AT_SYMLINK_NOFOLLOW, STATX_BTIME, &stx);
	if (rc == 0) {
		if (stx.stx_btime.tv_sec != 0) {
			printf("%u.%u\n", stx.stx_btime.tv_sec, stx.stx_btime.tv_nsec);
		} else {
			printf("-\n");
		}
	} else {
		perror("statx");
	}
	return rc;
}
