import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.util.ArrayList;
import java.util.List;

import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;

@SuppressWarnings("serial")
public class Krogi extends JFrame {

   private List<Krog> krogi;

   public Krogi() {
      super();
      krogi = new ArrayList<Krog>();

      setTitle("Krogi");
      setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
      setPreferredSize(new Dimension(800, 600));
      setMinimumSize(new Dimension(600, 450));
      setLayout(new BorderLayout());

      JPanel nadzornik = new JPanel();
      add(nadzornik, BorderLayout.NORTH);

      

      JPanel platno = new JPanel(){
         @Override
         protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            for (Krog krog : krogi) {
               int x = (int) (krog.getX());
               int y = (int) (krog.getY());
               int polmer = krog.getPolmer();
               Color barva = krog.getBarva();
               if (krog instanceof Kvadrat) {
                           
                  g.setColor(barva);
                  g.fillRect(x - polmer, y - polmer, 2 * polmer, 2 * polmer);
                           
                  g.setColor(Color.BLACK);
                  g.drawRect(x - polmer, y - polmer, 2 * polmer, 2 * polmer);
               } else {
                  
                  
                  g.setColor(barva);
                  g.fillOval(x - polmer, y - polmer, 2 * polmer, 2 * polmer);

                  g.setColor(Color.BLACK);
                  g.drawOval(x - polmer, y - polmer, 2 * polmer, 2 * polmer);
               }
               
            }
         }
      };

      JButton btnZbrisi = new JButton("Zbriši");
      btnZbrisi.addActionListener(new ActionListener() {
         public void actionPerformed(ActionEvent e) {
            krogi.clear();
            platno.repaint();
         }
      });

      nadzornik.add(btnZbrisi);

      nadzornik.add(new JLabel("    Barva:"));
      JComboBox<String> barve = new JComboBox<String>(new String[] { "Rdeča", "Zelena", "Modra" });
      nadzornik.add(barve);

      nadzornik.add(new JLabel("    Polmer:"));
      JComboBox<Integer> polmeri = new JComboBox<Integer>(new Integer[] { 8, 16, 32, 64 });
      nadzornik.add(polmeri);

      // Nevem cist tocno ali je bilo treba risati tudi med tem ko premikamo mis
      /*platno.addMouseMotionListener(new MouseMotionAdapter() {
         @Override
         public void mouseDragged(MouseEvent e) {
             int x = e.getX();
             int y = e.getY();
             int polmer = (int) polmeri.getSelectedItem();
             Color barva = null;
             switch (barve.getSelectedIndex()) {
             case 0:
                 barva = Color.RED;
                 break;
             case 1:
                 barva = Color.GREEN;
                 break;
             case 2:
                 barva = Color.BLUE;
                 break;
             }
             if (Math.random() < 0.5) {
               krogi.add(new Krog(x, y, polmer, barva));
            }
            else {
               krogi.add(new Kvadrat(x, y, polmer, barva));
            }
             System.out.println("Krog: x=" + x + ", y=" + y + ", polmer=" + polmer + ", barva=" + barva);
             platno.repaint();
         }
     });*/

      platno.addMouseListener(new MouseListener() {
         @Override
         public void mouseClicked(MouseEvent e){
            int x = e.getX();
            int y = e.getY();
            int polmer = (int) polmeri.getSelectedItem();
            Color barva = null;
            switch (barve.getSelectedIndex()) {
            case 0:
               barva = Color.RED;
               break;
            case 1:
               barva = Color.GREEN;
               break;
            case 2:
               barva = Color.BLUE;
               break;
            }
            if (Math.random() < 0.5) {
               krogi.add(new Krog(x, y, polmer, barva));
            }
            else {
               krogi.add(new Kvadrat(x, y, polmer, barva));
            }
            System.out.println("Krog: x=" + x + ", y=" + y + ", polmer=" + polmer + ", barva=" + barva);
            platno.repaint();

         }
         @Override
		   public void mouseEntered(MouseEvent e) {}
		   @Override
		   public void mouseExited(MouseEvent e) {}
		   @Override
		   public void mousePressed(MouseEvent e) {}
		   @Override
		   public void mouseReleased(MouseEvent e) {}
		   }
         );
      

      platno.setBackground(Color.WHITE);
      add(platno, BorderLayout.CENTER);
      }

      

   public static void main(String[] args) {
      new Krogi().setVisible(true);
   }
}

class Krog {
	
   private double x;
   private double y;
   private int polmer;
   private Color barva;

   public Krog(double x, double y, int polmer, Color barva) {
      super();
      this.x = x;
      this.y = y;
      this.polmer = polmer;
      this.barva = barva;
   }

   public double getX() {
      return x;
   }

   public double getY() {
      return y;
   }

   public int getPolmer() {
      return polmer;
   }

   public Color getBarva() {
      return barva;
   }
}

class Kvadrat extends Krog{
   public Kvadrat(double x, double y, int polmer, Color barva) {
		super(x, y, polmer, barva);
	}
}