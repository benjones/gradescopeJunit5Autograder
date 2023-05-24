package edu.utah.cs.autograder;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;


//adapted from the https://github.com/ucsb-gradescope-tools/jh61b version
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.METHOD})
public @interface GradedTest {
    String name() default "Unnamed test";
    double max_score() default 1;
    String visibility() default "visible";
    public static final String afterDueDate = "after_due_date";
}
