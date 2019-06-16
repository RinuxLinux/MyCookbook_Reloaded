<p align="center">
  <img src="https://cloud.githubusercontent.com/assets/2059754/24601246/753a7f36-1858-11e7-9d6b-7a0e64fb27f7.png" alt="bash logo"/>
</p>

## Table of Contents
  1. [Basic Operations](#1-basic-operations)  
    1.1. [File Operations](#11-file-operations)  
  2. [Basic Shell Programming](#2-basic-shell-programming)  
    2.1. [Variables](#21-variables)  
    2.2. [Array](#22-array)  
  3. [Tricks](#3-tricks)  
  4. [Debugging](#4-debugging)  
  

# 1. Basic Operations

### a. `export`
Displays all environment variables. If you want to get details of a specific variable, use `echo $VARIABLE_NAME`.  
```bash
export
```
Example:
```bash
$ export
AWS_HOME=/Users/adnanadnan/.aws
LANG=en_US.UTF-8
LC_CTYPE=en_US.UTF-8
LESS=-R

$ echo $AWS_HOME
/Users/adnanadnan/.aws
```

### b. `whatis`
whatis shows description for user commands, system calls, library functions, and others in manual pages
```bash
whatis something
```
Example:
```bash
$ whatis bash
bash (1)             - GNU Bourne-Again SHell
```

### e. clear
Clears content on window.

## 1.1. File Operations
<table>
   <tr>
      <td><a href="#a-cat">cat</a></td>
      <td><a href="#b-chmod">chmod</a></td>
      <td><a href="#k-head">head</a></td>
   </tr>
   <tr>
      <td><a href="#l-lpq">lpq</a></td>
      <td><a href="#m-lpr">lpr</a></td>
      <td><a href="#t-touch">touch</a></td>
   </tr>
</table>

### a. `cat`
It can be used for the following purposes under UNIX or Linux.  
* Display text files on screen
* Copy text files  
* Combine text files  
* Create new text files  
```bash
cat filename
cat file1 file2 
cat file1 file2 > newcombinedfile
cat < file1 > file2 #copy file1 to file2
```

### o. `ls`
Lists your files. `ls` has many options: `-l` lists files in 'long format', which contains the exact size of the file, who owns the file, who has the right to look at it, and when it was last modified. `-a` lists all files, including hidden files. For more information on this command check this [link](https://ss64.com/bash/ls.html).  
```bash
ls option
```
Example:
<pre>
$ ls -la
rwxr-xr-x   33 adnan  staff    1122 Mar 27 18:44 .
drwxrwxrwx  60 adnan  staff    2040 Mar 21 15:06 ..
-rw-r--r--@  1 adnan  staff   14340 Mar 23 15:05 .DS_Store
drwxr-xr-x  17 adnan  staff     578 Mar 27 23:36 .git
-rwxr-xr-x   1 adnan  staff    2702 Mar 25 18:08 .gitignore
</pre>


### t. `touch`
Updates access and modification time stamps of your file. If it doesn't exists, it'll be created.
```bash
touch filename
```
Example:
```bash
$ touch trick.md
```

## 1.2. Text Operations

<table>
    <tr>
      <td><a href="#a-awk">awk</a></td>
      <td><a href="#i-sed">sed</a></td>
      <td><a href="#j-sort">sort</a></td>
   </tr>
   <tr>
      <td><a href="#k-tr">tr</a></td>
      <td><a href="#l-uniq">uniq</a></td>
      <td><a href="#m-wc">wc</a></td>
   </tr>
</table>

### a. `awk`
awk is the most useful command for handling text files. It operates on an entire file line by line. By default it uses whitespace to separate the fields. The most common syntax for awk command is

```bash
awk '/search_pattern/ { action_to_take_if_pattern_matches; }' file_to_parse
```

Lets take following file `/etc/passwd`. Here's the sample data that this file contains:
```
root:x:0:0:root:/root:/usr/bin/zsh
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
```
So now lets get only username from this file. Where `-F` specifies that on which base we are going to separate the fields. In our case it's `:`. `{ print $1 }` means print out the first matching field.
```bash
awk -F':' '{ print $1 }' /etc/passwd
```
After running the above command you will get following output.
```
root
daemon
bin
sys
sync
```
For more detail on how to use `awk`, check following [link](https://www.cyberciti.biz/faq/bash-scripting-using-awk).


### b. `cut`
Remove sections from each line of files

*example.txt*
```bash
red riding hood went to the park to play
```

*show me columns 2 , 7 , and 9 with a space as a separator*
```bash
cut -d " " -f2,7,9 example.txt
```
```bash
riding park play
```

### c. `echo`
Display a line of text

*display "Hello World"*
```bash
echo Hello World
```
```bash
Hello World
```

*display "Hello World" with newlines between words*
```bash
echo -ne "Hello\nWorld\n"
```
```bash
Hello
World
```


*display lines that have either "Lorem" or "dolor" in them.*
```bash
egrep '(Lorem|dolor)' example.txt
or
grep -E '(Lorem|dolor)' example.txt
```
```bash
Lorem ipsum
dolor sit amet,
et dolore magna
duo dolores et ea
sanctus est Lorem
ipsum dolor sit
```


*show example.txt with line numbers*
```bash
nl -s". " example.txt 
```
```bash
     1. Lorem ipsum
     2. dolor sit amet,
     3. consetetur
     4. sadipscing elitr,
     5. sed diam nonumy
     6. eirmod tempor
     7. invidunt ut labore
     8. et dolore magna
     9. aliquyam erat, sed
    10. diam voluptua. At
    11. vero eos et
    12. accusam et justo
    13. duo dolores et ea
    14. rebum. Stet clita
    15. kasd gubergren,
    16. no sea takimata
    17. sanctus est Lorem
    18. ipsum dolor sit
    19. amet.
```

## 1.3. Directory Operations

<table>
   <tr>
      <td><a href="#a-cd">cd</a></td>
      <td><a href="#b-mkdir">mkdir</a></td>
      <td><a href="#c-pwd">pwd</a></td>
   </tr>
</table>


## 1.4. SSH, System Info & Network Operations

<table>
   <tr>
      <td><a href="#a-bg">bg</a></td>
      <td><a href="#b-cal">cal</a></td>
      <td><a href="#j-last">last</a></td>
   </tr>
   <tr>
      <td><a href="#k-man">man</a></td>
      <td><a href="#s-uname">uname</a></td>
      <td><a href="#t-uptime">uptime</a></td>
   </tr>
   <tr>
      <td><a href="#u-w">w</a></td>
      <td><a href="#x-whois">whois</a></td>
   </tr>
</table>


### p. `scp`
Transfer files between a local host and a remote host or between two remote hosts.

*copy from local host to remote host*
```bash
scp source_file user@host:directory/target_file
```
*copy from remote host to local host*
```bash
scp user@host:directory/source_file target_file
scp -r user@host:directory/source_folder target_folder
```
This command also accepts an option `-P` that can be used to connect to specific port.  
```bash
scp -P port user@host:directory/source_file target_file
```


## 1.5. Process Monitoring Operations

<table>
   <tr>
      <td><a href="#a-kill">kill</a></td>
      <td><a href="#b-killall">killall</a></td>
      <td><a href="#c-&">&amp;</a></td>
      <td><a href="#d-nohup">nohup</a></td>
   </tr>
</table>

### a. `kill`
Kills (ends) the processes with the ID you gave.  
```bash
kill PID
```


# 2. Basic Shell Programming


The first line that you will write in bash script files is called `shebang`. This line in any script determines the script's ability to be executed like a standalone executable without typing sh, bash, python, php etc beforehand in the terminal.

```bash
#!/usr/bin/env bash
```

## 2.1. Variables

Creating variables in bash is similar to other languages. There are no data types. A variable in bash can contain a number, a character, a string of characters, etc. You have no need to declare a variable, just assigning a value to its reference will create it.

Example:
```bash
str="hello world"
```

The above line creates a variable `str` and assigns "hello world" to it. The value of variable is retrieved by putting the `$` in the beginning of variable name.

Example:
```bash
echo $str   # hello world
```
## 2.2. Array
Like other languages bash has also arrays. An array is variable containing multiple values. There's no maximum limit on the size of array. Array in bash are zero based. The first element is indexed with element 0. There are several ways for creating arrays in bash. Which are given below.

Examples:
```bash
array[0] = val
array[1] = val
array[2] = val
array=([2]=val [0]=val [1]=val)
array=(val val val)
```
To display a value at specific index use following syntax:

```bash
${array[i]}     # where i is the index
```

If no index is supplied, array element 0 is assumed. To find out how many values there are in the array use the following syntax:

```bash
${#array[@]}
```

Bash has also support for the ternary conditions. Check some examples below.

```bash
${varname:-word}    # if varname exists and isn't null, return its value; otherwise return word
${varname:=word}    # if varname exists and isn't null, return its value; otherwise set it word and then return its value
${varname:+word}    # if varname exists and isn't null, return word; otherwise return null
${varname:offset:length}    # performs substring expansion. It returns the substring of $varname starting at offset and up to length characters
```

## 2.3 String Substitution

Check some of the syntax on how to manipulate strings

```bash
${variable#pattern}         # if the pattern matches the beginning of the variable's value, delete the shortest part that matches and return the rest
${variable##pattern}        # if the pattern matches the beginning of the variable's value, delete the longest part that matches and return the rest
${variable%pattern}         # if the pattern matches the end of the variable's value, delete the shortest part that matches and return the rest
${variable%%pattern}        # if the pattern matches the end of the variable's value, delete the longest part that matches and return the rest
${variable/pattern/string}  # the longest match to pattern in variable is replaced by string. Only the first match is replaced
${variable//pattern/string} # the longest match to pattern in variable is replaced by string. All matches are replaced
${#varname}     # returns the length of the value of the variable as a character string
```

## 2.4. Functions
As in almost any programming language, you can use functions to group pieces of code in a more logical way or practice the divine art of recursion. Declaring a function is just a matter of writing function my_func { my_code }. Calling a function is just like calling another program, you just write its name.

```bash
function name() {
    shell commands
}
```

Example:
```bash
#!/bin/bash
function hello {
   echo world!
}
hello

function say {
    echo $1
}
say "hello world!"
```

When you run the above example the `hello` function will output "world!". The above two functions `hello` and `say` are identical. The main difference is function `say`. This function, prints the first argument it receives. Arguments, within functions, are treated in the same manner as arguments given to the script.

## 2.5. Conditionals

The conditional statement in bash is similar to other programming languages. Conditions have many form like the most basic form is `if` expression `then` statement where statement is only executed if expression is true.

```bash
if [ expression ]; then
    will execute only if expression is true
else
    will execute if expression is false
fi
```

Sometime if conditions becoming confusing so you can write the same condition using the `case statements`.

```bash
case expression in
    pattern1 )
        statements ;;
    pattern2 )
        statements ;;
    ...
esac
```

Expression Examples:

```bash
statement1 && statement2  # both statements are true
statement1 || statement2  # at least one of the statements is true

str1=str2       # str1 matches str2
str1!=str2      # str1 does not match str2
str1<str2       # str1 is less than str2
str1>str2       # str1 is greater than str2
-n str1         # str1 is not null (has length greater than 0)
-z str1         # str1 is null (has length 0)

-a file         # file exists
-d file         # file exists and is a directory
-e file         # file exists; same -a
-f file         # file exists and is a regular file (i.e., not a directory or other special type of file)
-r file         # you have read permission
-s file         # file exists and is not empty
-w file         # you have write permission
-x file         # you have execute permission on file, or directory search permission if it is a directory
-N file         # file was modified since it was last read
-O file         # you own file
-G file         # file's group ID matches yours (or one of yours, if you are in multiple groups)

file1 -nt file2     # file1 is newer than file2
file1 -ot file2     # file1 is older than file2

-lt     # less than
-le     # less than or equal
-eq     # equal
-ge     # greater than or equal
-gt     # greater than
-ne     # not equal
```

## 2.6. Loops

There are three types of loops in bash. `for`, `while` and `until`.

Different `for` Syntax:
```bash
for x := 1 to 10 do
begin
  statements
end

for name [in list]
do
  statements that can use $name
done

for (( initialisation ; ending condition ; update ))
do
  statements...
done
```

`while` Syntax:
```bash
while condition; do
  statements
done
```

`until` Syntax:
```bash
until condition; do
  statements
done
```

# 3. Tricks

## Set an alias
Open `bash_profile` by running following command `nano ~/.bash_profile`
> alias dockerlogin='ssh www-data@adnan.local -p2222'  # add your alias in .bash_profile

## To quickly go to a specific directory
nano ~/.bashrc
> export hotellogs="/workspace/hotel-api/storage/logs"

```bash
source ~/.bashrc
cd $hotellogs
```

## Exit traps

Make your bash scripts more robust by reliably performing cleanup.

```bash
function finish {
  # your cleanup here. e.g. kill any forked processes
  jobs -p | xargs kill
}
trap finish EXIT
```

## Saving your environment variables

When you do `export FOO = BAR`, your variable is only exported in this current shell and all its children, to persist in the future you can simply append in your `~/.bash_profile` file the command to export your variable
```bash
echo export FOO=BAR >> ~/.bash_profile
```

## Accessing your scripts

You can easily access your scripts by creating a bin folder in your home with `mkdir ~/bin`, now all the scripts you put in this folder you can access in any directory.

If you can not access, try append the code below in your `~/.bash_profile` file and after do `source ~/.bash_profile`.
```bash
    # set PATH so it includes user's private bin if it exists
    if [ -d "$HOME/bin" ] ; then
        PATH="$HOME/bin:$PATH"
    fi
```

# 4. Debugging
You can easily debug the bash script by passing different options to `bash` command. For example `-n` will not run commands and check for syntax errors only. `-v` echo commands before running them. `-x` echo commands after command-line processing.

```bash
bash -n scriptname
bash -v scriptname
bash -x scriptname
```

## Contribution

- Report issues [How to](https://help.github.com/articles/creating-an-issue/)
- Open pull request with improvements [How to](https://help.github.com/articles/about-pull-requests/)
- Spread the word

## Translation
- [Chinese | 简体中文](https://github.com/vuuihc/bash-guide)
- [Turkish | Türkçe](https://github.com/omergulen/bash-guide)
- [Japanese | 日本語](https://github.com/itooww/bash-guide)

## License

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
