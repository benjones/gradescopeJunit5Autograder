package PACKAGE_NAME;

//the annotations required for generating gradescope JSON
import edu.utah.cs.autograder.AutograderWatcher;
import edu.utah.cs.autograder.GradedTest;
//Junit 5 stuff
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;
import org.junit.jupiter.api.extension.ExtendWith;

import java.util.Arrays;
import java.util.Random;

import static org.junit.jupiter.api.Assertions.assertEquals;

//make all tests timeout after 10 seconds
@Timeout(10)
//register this with the class that scores tests
@ExtendWith(AutograderWatcher.class)
public class AutograderTests {

    private static final double pointsPerTest = 0.5;

    //pre test, always visible to students (this is the default)
    @Test
    @GradedTest(name = "Test for short list", max_score = pointsPerTest )
    void medianTest(){
        var arr = new int[]{5,1,2,3,4};
        assertEquals(3, Median.median(arr));
    }

    //post test, test results only visible after due date
    @Test
    @GradedTest(name = "Test for short list", max_score = pointsPerTest, visibility = GradedTest.afterDueDate)
    void medianTest(){
        var arr = new int[]{5,1,2,3,4};
        assertEquals(3, Median.median(arr));
    }
}
