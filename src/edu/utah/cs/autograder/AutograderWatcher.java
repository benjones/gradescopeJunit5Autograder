package edu.utah.cs.autograder;

import org.junit.jupiter.api.extension.AfterAllCallback;
import org.junit.jupiter.api.extension.AfterTestExecutionCallback;
import org.junit.jupiter.api.extension.ExtensionContext;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;

public class AutograderWatcher implements AfterTestExecutionCallback, AfterAllCallback {
    StudentResults results = new StudentResults();
    @Override
    public void afterTestExecution(ExtensionContext context){
        System.out.println("completed: " + context.getDisplayName());
        var method = context.getTestMethod().get();
        var gradedTest = method.getAnnotation(GradedTest.class);
        if(gradedTest != null) {
            boolean passed = context.getExecutionException().isEmpty();
            results.addResult(new StudentResults.TestResult(gradedTest.name(),
                    passed ? "" : context.getExecutionException().get().getMessage(),
                    gradedTest.max_score(), passed, gradedTest.visibility()));
        }
    }

    @Override
    public void afterAll(ExtensionContext extensionContext) throws Exception {
        var resultsDir = new File("/autograder/results");
        resultsDir.mkdir();
        var resultsFile = new File("/autograder/results/results.json");
        Files.write(resultsFile.toPath(), results.toJSON().getBytes());
        System.out.println("results saved to " + resultsFile.getAbsolutePath());
        System.out.println(results.toJSON());
    }
}
