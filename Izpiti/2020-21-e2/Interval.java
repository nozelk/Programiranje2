import java.util.Arrays;
import java.util.List;

public class Interval{
    int lower, upper;


    public Interval(int lower, int upper){
        this.lower = lower;
        this.upper = upper;
    }

    @Override
    public String toString() {
        return "[" + lower + ", " + upper + "]";
    }

    public boolean includes(int number){
        return lower <= number && number <= upper;
    }

    public boolean includes(List<Integer> numbers){
        for(int num : numbers){
            if (!includes(num)){
                return false;
            }
        }
        return true;
    }

    public boolean includes(Interval interval){
        return this.lower <= interval.lower && interval.upper <= this.upper;
    }

    public static Interval merge(Interval first, Interval second){
        int lowerM = Math.min(first.lower, second.lower);
        int upperM = Math.max(first.upper, second.upper);
        return new Interval(lowerM, upperM);
    }

    public static void main(String[] args){
        Interval interval = new Interval(2, 7);
        System.out.println(interval);
        System.out.println(interval.includes(4));
        System.out.println(interval.includes(Arrays.asList(new Integer[] {3, 4, 5})));
        System.out.println(interval.includes(new Interval(-1, 5)));
        System.out.println(Interval.merge(interval, new Interval(5, 9)));
    }
}