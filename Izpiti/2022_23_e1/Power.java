public class Power implements Function {
    private final int exponent;

    public Power(int exponent) {
        this.exponent = exponent;
    }

    @Override
    public String function() {
        return "f(x) = x^" + exponent;
    }

    @Override
    public double function(double x) {
        return Math.pow(x, exponent);
    }

    @Override
    public String derivative() {
        return "f'(x) = " + exponent + "*x^" + (exponent - 1);
    }

    @Override
    public double derivative(double x) {
        return exponent * Math.pow(x, exponent - 1);
    }
}
