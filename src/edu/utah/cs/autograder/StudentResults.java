package edu.utah.cs.autograder;

import com.google.gson.GsonBuilder;

import java.util.ArrayList;

public class StudentResults {

    //chosen to match the gradescope JSON format
    String visibility = "after_due_date";
    String stdout_visibility = "after_due_date";

    ArrayList<TestResult> tests = new ArrayList<>();
    public static class TestResult {
       double score;
       double max_score;
       String status;
       String name;
       String output;

       String visibility;

        public TestResult(String name, String output, double max_score, boolean passed, String visibility){
            this.score = passed ? max_score : 0;
            this.max_score = max_score;
            this.status = passed ? "passed" : "failed";
            this.name = name;
            this.output = output;
            this.visibility = visibility;
        }

    }

    public void addResult(TestResult result){
        tests.add(result);
    }

    public String toJSON(){
        //use the builder to pretty print
        return (new GsonBuilder()).setPrettyPrinting().create().toJson(this);
    }
}
