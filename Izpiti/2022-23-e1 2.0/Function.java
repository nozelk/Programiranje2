

public interface Function{
    public String function();
    public double function(double x);
    public String derivative();
    public double derivative(double x);

    public static void main(String[] args) {
		Function[]	functions	= new Function[] { new Exponential(), new Power(3), new Linear() };
		

		
		for (Function	function:	functions) {
						System.out.println(function.function());
						System.out.println("f(1) =	" +	function.function(1.0));
						System.out.println(function.derivative());
						System.out.println("f'(1) =	" +	function.derivative(1.0));
						System.out.println();
		}
	}
}