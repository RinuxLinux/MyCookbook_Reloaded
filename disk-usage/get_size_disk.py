
import os

def get_size_in_HR(size,precision=2):
	"""
	Get Human Readable size
	@usage   get_size_in_HR(get_size_in_bytes(file), 2)
	"""
	suffixes=['B','KB','MB','GB','TB']
	suffixIndex = 0
	while size > 1024:
		suffixIndex += 1 		#increment the index of the suffix
		size = size/1024.0 		#apply the division
	return "%.*f %s" % (precision,size,suffixes[suffixIndex])



def disk_usage(path):
    """Return disk usage statistics about the given path.

    Returned valus is a named tuple with attributes 'total', 'used' and
    'free', which are the amount of total, used and free space, in bytes.
    """
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return total, used, free


disque = '/media/reno/MEDIA'
disque = 'F:\\'
total, used, free = disk_usage(disque)
percent_used = used * 100 / total	
total_HR = get_size_in_HR(total,precision=2)
used_HR  = get_size_in_HR(used,precision=2)
free_HR  = get_size_in_HR(free,precision=2)

