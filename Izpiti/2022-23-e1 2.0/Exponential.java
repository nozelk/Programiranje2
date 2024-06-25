public class Exponential implements Function {
    
    public String function() {
        return "f(x) = e^x";
    }

    public double function(double x) {
        return Math.exp(x);
    }

    public String derivative() {
        return "f'(x) = e^x";
    }

    public double derivative(double x) {
        return Math.exp(x);
    }
}