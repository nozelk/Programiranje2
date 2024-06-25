import java.util.Arrays;

public interface Function extends Comparable<Function> {
    String function();
    double function(double x);
    String derivative();
    double derivative(double x);
    
    @Override
    default int compareTo(Function other) {
        int result = Double.compare(this.function(1.0), other.function(1.0));
        if (result == 0) {
            result = Double.compare(this.derivative(1.0), other.derivative(1.0));
        }
        return result;
    }

    public static void main(String[] args) {
        Function[] functions = new Function[] { new Exponential(), new Power(3), new Linear() };
        Arrays.sort(functions); // Urejanje funkcij

        for (Function function: functions) {
            System.out.println(function.function());
            System.out.println("f(1) = " + function.function(1.0));
            System.out.println(function.derivative());
            System.out.println("f'(1) = " + function.derivative(1.0));
            System.out.println();
        }
    }
}
