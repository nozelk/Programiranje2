import java.io.*;

class PrometSkoziPredorGolovec{
    public static void main(String[] args){
        try {
            System.out.println(speeding(new File("golovec.txt"), new File("speeding.txt"), 622, 80.0));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static int speeding(File in, File out, int distance, double limit) throws IOException{
        BufferedReader reader = new BufferedReader(new FileReader(in));
        BufferedWriter writer = new BufferedWriter(new FileWriter(out));
        int prekrski = 0;

        String vrstica;
        while ((vrstica = reader.readLine()) != null) {
            vrstica = vrstica.trim();
            String[] tab = vrstica.split(" ");
            int start = Integer.parseInt(tab[0]);
            int finish = Integer.parseInt(tab[1]);
            Drive drive = new Drive(start, finish, distance, tab[2]);
            if (drive.getSpeed() > limit){
                prekrski++;
                String formattedSpeed = String.format("%.2f", drive.getSpeed());
                writer.write(drive.getRegistration() + " " + formattedSpeed.replace(',','.') + "\n");
                
            }

        }

        reader.close();
        writer.flush(); 
        writer.close();
        return prekrski;
    }

}


class Drive{
    
    private int start;
    private int finish;
    private int distance;
    private String registration;


    public Drive(int start, int finish, int distance, String registration){
        this.start = start;
        this.finish = finish;
        this.distance = distance;
        this.registration = registration;
    }
    public int getStart(){
        return start;
    }
    public int getFinish(){
        return finish;
    }
    public int getDistacne(){
        return distance;
    }
    public String getRegistration(){
        return registration;
    }
    public double getSpeed(){
        return 3.6 * distance / (finish - start);
    }
}