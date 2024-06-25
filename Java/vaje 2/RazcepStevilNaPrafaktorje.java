import java.util.HashMap;
import java.util.Map;
import java.util.*;

public class RazcepStevilNaPrafaktorje {

    public static int divisor(int n){
        for (int i = 2; i <= Math.sqrt(n); i++){
            if (n % i == 0){
                return i;
            }
        }
        return n;
    }

    public static Map<Integer, Integer> factorize(int n){
        Map<Integer, Integer> map = new TreeMap<>();
        while (n > 1){
            int deljitelj = divisor(n);
            n /= deljitelj;
            map.put(deljitelj, map.getOrDefault(deljitelj, 0) + 1);
        }
        map.remove(1);
        return map;
    }
    
    public static void factorization(int number) {
		Map<Integer, Integer> map = factorize(number);
		String str = number + " = " ;
		for (Integer key : map.keySet()) {
		    int value = map.get(key);
		    if (value != 1)
		    str +=  key + "^" + value+ " * ";
		    else
		    str += key + " * ";
		}    
		String strKoncni = str.substring(0, str.length()-2) ; //odrezem zadnjo *
		System.out.println(strKoncni);
			
	}
    
    
    public static void main(String[] args) {
        factorization(5);
        factorization(16);
        factorization(43);
        factorization(99);
        factorization(1025);
        factorization(4382);
        factorization(74438);
        factorization(578298);
        factorization(5761665);

    }
}
