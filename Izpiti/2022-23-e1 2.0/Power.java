
public class Power implements Function{
    private int exponent;

    public Power(int exponent) {
        this.exponent = exponent;
    }

    public String function() {
        return "f(x) = x^" + exponent;
    }

    public double function(double x) {
        return Math.pow(x, exponent);
    }

    public String derivative() {
        return "f'(x) = " + exponent + "*x^" + (exponent - 1);
    }

    public double derivative(double x) {
        return exponent * Math.pow(x, exponent - 1);
    }
}
