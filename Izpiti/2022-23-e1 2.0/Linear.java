public class Linear implements Function{
	
	public String function() {
		return "f(x) = x";
	}

	public double function(double x) {
		return x;
	}

	public String derivative() {
		return "f'(x) = 1";
	}
    
	public double derivative(double x) {
		return 1.0f;
	}
	
}