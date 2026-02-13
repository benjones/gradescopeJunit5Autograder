package edu.utah.cs.autograder;

import com.google.gson.Gson;
import com.google.gson.stream.JsonReader;

import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.Method;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;

public class MethodSignatureChecker {

    /**
     * String based representation of an expected method signature
     *
     * @param name       method className
     * @param returnType as a string
     * @param args       arg types as strings
     */
    public static record Signature(String name, String returnType, String[] args) {
    }

    public static record ClassSignature(String className, Signature[] methods) {
    }

    /**
     * Writes failing autograder output to the place where gradescope wants it and returns a failing exit code
     * @param error message saying what the student did wrong
     */
    private static void makeAutograderOutput(String error) {
        //try to write to /autograder/results/results.json
        //but just print it if that fails
        String result = String.format("""
                { "score": 0.0,");
                  "stdout_visibility": "visible",
                  "output": "%s 
                  Because of this all autograder tests failed and you are currently getting zero autograder points."
                  }
                """, error);

        try {
            var resultsDir = new File("/autograder/results");
            resultsDir.mkdir();
            var resultsFile = new File("/autograder/results/results.json");

            Files.write(resultsFile.toPath(), result.getBytes());
            System.out.println("results saved to " + resultsFile.getAbsolutePath());
        } catch (IOException e) {
            //couldn't make /autograder, so probably running locally for testing without uploading
            //TODO make it easier to pass the JSON method description here...
            System.out.println("couldn't make /autograder/results folder, just printing the results");
        }
        System.out.println(result);

        System.exit(-1);
    }

    private static String transformType(String raw) {
        return switch (raw) {
            case "class [D" -> "double array";
            case "class [I" -> "int array";
            case "class [B" -> "boolean array";
            case "class java.lang.String" -> "String";
            default -> raw;
        };
    }

    /**
     * Takes in an expected method signature of the form
     * Signature("methodName", "return type", {"paramType1", "paramType2"})
     * and checks it against actual methods of a particular class
     * <p>
     * Creates an error message and stops if there is a mismatch.
     *
     * @param signature signature to check
     * @param clazz     the class to check for signature in
     */
    private static void checkMethod(Signature signature, Class<?> clazz) {
        String errorMessage = "Could not find a method called " + signature.name;

        for (Method method : clazz.getMethods()) {
            if (signature.name.equals(method.getName())) {
                errorMessage = "";
                //check param list length
                Class<?>[] parameterTypes = method.getParameterTypes();
                if (parameterTypes.length != signature.args.length) {
                    errorMessage = "For method " + signature.name +
                            " the autograder is expecting " + signature.args.length +
                            " parameters but instead found " + parameterTypes.length;
                    continue;
                }
                //check param types
                for (int index = 0; index < signature.args.length; index++) {
                    String param = parameterTypes[index].toString();
                    String expectedParam = signature.args[index];
                    if (!param.equals(expectedParam)) {
                        errorMessage = "For method " + signature.name +
                                " the autograder is expecting a parameter type " +
                                transformType(signature.args[index]) +
                                " in location " + index + " of the parameter list, but found "
                                + transformType(param) + " instead";
                    }
                }
                // check return type
                String actualReturn = method.getReturnType().toString();
                if (!actualReturn.equals(signature.returnType)) {
                    errorMessage = "For method " + signature.name +
                            " the autograder is expecting a return type " +
                            transformType(signature.returnType) +
                            " but found "
                            + transformType(actualReturn) + " instead";
                }
                //If it gets here with an empty error message, the correct method was found.
                if (errorMessage.isEmpty())
                    break;
            }
        }
        // Went through the class methods and could not find an expected one.
        if (!errorMessage.isEmpty()) {
            makeAutograderOutput(errorMessage);
        }
    }


    public static void main(String[] args) throws IOException, ClassNotFoundException {

        System.out.println("Reading class descriptions from stdin");
        var reader = new JsonReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
        var gson = new Gson();
        ClassSignature[] classSignatures = gson.fromJson(reader, ClassSignature[].class);

        for (var classSig : classSignatures) {
            var clazz = Class.forName(classSig.className);
            var methodSigs = classSig.methods;

            // Check each signature
            for (var signature : methodSigs)
                checkMethod(signature, clazz);
        }
        // If it survives here, there is no output.
        //we exit with success return code, so run_autograder keeps going
    }

}
