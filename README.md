# Java Autograder for Gradescope with Junit 5

This repo includes classes + running instructions to use Junit5 tests with a gradescope autograder

## Instructions

Download .jar files for junit-platform-console-standalone and gson (I think I got them from mvnrepository.com)
and stick them in the top level folder of autograder folder (root of this git repo if you cloned it)

modify the run_autograder script with to specify the package name students should be using and the files they should submit.
If the version numbers of the junit/gson .jars has changed, update those as well (there's 2 places)

Write your tests, which should be in the same package as student code, probably.  See SampleAutograderTests.java
to see what they should look like.

Zip up all the stuff in this folder (not the folder itself) to upload to gradescope

Now we're ready to go to "configure autograder" on gradescope

I use the gradescope container image with a JDK already installed, so I don't need to do any apt-get installation stuff
The latest version was JDK17 last I checked, which seems to be new-enough.

The setup.sh script does nothing because there's no packages to install.  It's included so that gradescope doesn't
crash trying to run it (it might not be necessary)

That should be it.  PR's or emails (benjones@cs.utah.edu) are welcome if you have questions/concerns/improvements

