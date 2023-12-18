# Java Autograder for Gradescope with Junit 5

This repo includes classes + running instructions to use Junit5 tests with a gradescope autograder

## Workflow

This tool is set up to follow the workflow that I found most useful when creating autograders:

* Write my solution, as if I'm a student in the appropriate package, etc
* Write unittests which will be used for autograding in that project (typically in a different package).  To set them up to grade with this tool, add the `edu.utah.cs.autograder` package and all the classes in it to your project, then annotate your tests.
* Write an assignment description JSON file, mostly likely by copying the sample included here.  This should go in your project root (ie in the folder containing src).  This specifies which files you expect students to submit, what handout files should be included in the autograder, and what extra JARs to include if any (I always include one for GSON and the JUnit runner)
* Run the `release.py` script which will zip up all the necessary files and write a script to be run by the autograder to
  * copy files to the right place
  * compile the student submission (and output compiler errors if it fails)
  * run the autograder tests
  * produce the appropriate JSON file reporting results to Gradescope
* Upload the zip file to Gradecope, making sure that you use a VM with the most recent JDK preinstalled (JDK 17 as of writing this)

## More detailed Instructions

Once your solution is written:

Download .jar files for junit-platform-console-standalone and gson (I think I got them from mvnrepository.com)
and stick them in the top level folder of your project.  If you want to test the autograder on your own solution, you'll need to add GSON to your project as well.  It should run the unittests and print info about the autograder score, including the total number of possible points.


Write your tests.  I usually put them in a different package (like `autogradertests` or similar).  These are normal JUnit5 tests which you add extra annotations to.  See the provided sample tests.  Note, currently only one test file can be used to produce tests, so you can't split the tests across multiple files (yet).  Also, these classes need to end with `Test` or `Tests` (if you don't, IntelliJ, at least, will warn you that your test class doesn't match some regex.  I believe this is a JUnit requirement).  

Edit your assignment properties JSON description (modify the sample provided below)

run `python3 release.py <your description json>` to produce a zip file.  The python script can be anywhere, but the CWD should be the top level of your project.  It needs to contain the src folder, any extra files you want to include, and the JARs you specify.

Now we're ready to go to "configure autograder" on gradescope

I use the gradescope container image with a JDK already installed, so I don't need to do any apt-get installation stuff
The latest version was JDK17 last I checked, which seems to be new-enough.

That should be it.  PR's or emails (benjones@cs.utah.edu) are welcome if you have questions/concerns/improvements

