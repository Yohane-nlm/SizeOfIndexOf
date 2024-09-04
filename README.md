# Description
This script is used to calculate the total file size of a 'index of' page with multi threads.

# Usage
`python SizeOfIndexOf.py -U <url> [-T <thread_num>]`

# Arguments
`-U, --url`: The url to the 'index of' page.

`-T, --threads`: The number of threads to use (10 for default).

# Example
`python SizeOfIndexOf.py -P http://example.com/ -T 10`