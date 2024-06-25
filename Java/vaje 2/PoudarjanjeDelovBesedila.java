public class PoudarjanjeDelovBesedila {
    
    public static String highlight(String s){
        String newOne = "";
        boolean  flag = false;
        for (char crka : s.toCharArray()){
            if (crka == '*'){
                if (flag){
                    flag = false;
                    continue;
                }
                else{
                    flag = true;
                    continue;
                }    
            }
            if (flag)
                newOne += Character.toUpperCase(crka);

            else
                newOne += crka;

        }
        return newOne;
    }
    public static void main(String[] args) {
        System.out.println(highlight("Poudarjena *beseda* in nepoudarjena beseda."));
        System.out.println(highlight("Poudarjeno *besedilo, ki se nadaljuje..."));
        System.out.println(highlight("Poudarjeno *besedilo*, ki se ne nadaljuje."));
        System.out.println(highlight("*g*it repozitorija *g*ithub in *b*it*b*ucket."));
        final String ABECEDA = "abcčdefghijklmnoprsštuvzž., ";
    	String random = "";
    	for (int i = 0; i < 40; i++)
    	   if (Math.random() < 0.1)
    	      random += "*";
    	   else
    	      random += ABECEDA.charAt((int)(Math.random() * ABECEDA.length()));
        System.out.println(random);
    	System.out.println(highlight(random));
    }
}
