public class Exponential implements Function {
    @Override
    public String function() {
        return "f(x) = e^x";
    }

    @Override
    public double function(double x) {
        return Math.exp(x);
    }

    @Override
    public String derivative() {
        return "f'(x) = e^x";
    }

    @Override
    public double derivative(double x) {
        return Math.exp(x);
    }
}
