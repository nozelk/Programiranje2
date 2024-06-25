import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public class Student implements Comparable<Student> {
    private String SID;
    private String name;
    private String surname;
    
    private static final String[] NAMES = {"Franc", "Janez", "Marko", "Marija", "Ana", "Maja"};
    private static final String[] SURNAMES = {"Novak", "Horvat", "Kovačič", "Krajnc", "Zupančič", "Kovač"};
    

    public Student(String SID, String name, String surname) {
        this.SID = SID;
        this.name = name;
        this.surname = surname;
    }
    

    public Student() {
        this.SID = generateSID();
        this.name = NAMES[new Random().nextInt(NAMES.length)];
        this.surname = SURNAMES[new Random().nextInt(SURNAMES.length)];
    }
    

    private String generateSID() {
        Random rand = new Random();
        int randomNumber = 100 + rand.nextInt(900);
        return "27191" + randomNumber;
    }
    

    public String getSID() {
        return SID;
    }
    
    public String getName() {
        return name;
    }
    
    public String getSurname() {
        return surname;
    }
    

    @Override
    public String toString() {
        return "[" + SID + "] " + name + " " + surname;
    }
    

    @Override
    public int compareTo(Student other) {
        return this.SID.compareTo(other.SID);
    }
    

    public static void main(String[] args) {
        List<Student> students = new ArrayList<Student>();
        for (int i = 0; i < 10; i++) {
            students.add(new Student());
        }
        
        Collections.sort(students); // Sorting students
        
        for (Student student : students) {
            System.out.println(student); // Printing student details
        }
    }
}
