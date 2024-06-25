public class Linear implements Function {
    @Override
    public String function() {
        return "f(x) = x";
    }

    @Override
    public double function(double x) {
        return x;
    }

    @Override
    public String derivative() {
        return "f'(x) = 1";
    }

    @Override
    public double derivative(double x) {
        return 1.0;
    }
}