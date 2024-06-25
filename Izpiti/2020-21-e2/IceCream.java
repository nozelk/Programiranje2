import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Point;
import java.awt.Rectangle;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

import javax.swing.JFrame;
import javax.swing.JPanel;

public class IceCream {

    enum Flavour {
        NONE, CHOCOLATE, STRAWBERRY, VANILLA
    }

    public static Flavour flavour = Flavour.NONE;

    public static void main(String[] args) {
        JFrame frame = new JFrame("Ice Cream");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(new Dimension(800, 600));
        frame.setResizable(true);

        JPanel panel = new IceCreamPanel();
        panel.setBackground(Color.WHITE);
        frame.add(panel);

        frame.setVisible(true);
    }

    static class IceCreamPanel extends JPanel {

        private Rectangle chocolateTub = new Rectangle(50, 400, 150, 150);
        private Rectangle strawberryTub = new Rectangle(250, 400, 150, 150);
        private Rectangle vanillaTub = new Rectangle(450, 400, 150, 150);
        private Point scoopPosition = null;
        private Flavour scoopFlavour = Flavour.NONE;

        public IceCreamPanel() {
            addMouseListener(new MouseAdapter() {
                @Override
                public void mouseClicked(MouseEvent e) {
                    Point p = e.getPoint();
                    if (chocolateTub.contains(p)) {
                        scoopFlavour = Flavour.CHOCOLATE;
                        scoopPosition = new Point(680, 400);
                    } else if (strawberryTub.contains(p)) {
                        scoopFlavour = Flavour.STRAWBERRY;
                        scoopPosition = new Point(680, 400);
                    } else if (vanillaTub.contains(p)) {
                        scoopFlavour = Flavour.VANILLA;
                        scoopPosition = new Point(680, 400);
                    } else {
                        scoopFlavour = Flavour.NONE;
                        scoopPosition = null;
                    }
                    repaint();
                }
            });
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);

            // Draw tubs
            g.setColor(new Color(123, 63, 0));
            g.fillRect(chocolateTub.x, chocolateTub.y, chocolateTub.width, chocolateTub.height);
            g.setColor(new Color(251, 41, 67));
            g.fillRect(strawberryTub.x, strawberryTub.y, strawberryTub.width, strawberryTub.height);
            g.setColor(new Color(243, 229, 171));
            g.fillRect(vanillaTub.x, vanillaTub.y, vanillaTub.width, vanillaTub.height);

            // Draw labels
            g.setColor(Color.WHITE);
            g.drawString("Chocolate", chocolateTub.x + 40, chocolateTub.y + 75);
            g.drawString("Strawberry", strawberryTub.x + 40, strawberryTub.y + 75);
            g.drawString("Vanilla", vanillaTub.x + 40, vanillaTub.y + 75);

            // Draw cone
            g.setColor(new Color(196,140,92));
            int[] xPoints = {640, 720, 680};
            int[] yPoints = {400, 400, 550};
            g.fillPolygon(xPoints, yPoints, 3);

            // Draw scoop if available
            if (scoopFlavour != Flavour.NONE) {
                switch (scoopFlavour) {
                    case CHOCOLATE:
                        g.setColor(new Color(123, 63, 0));
                        break;
                    case STRAWBERRY:
                        g.setColor(new Color(251, 41, 67));
                        break;
                    case VANILLA:
                        g.setColor(new Color(243, 229, 171));
                        break;
                }
                if (scoopPosition != null) {
                    g.fillArc(scoopPosition.x - 40, scoopPosition.y - 40, 80, 80, 0, 180);
                }
            }
        }
    }
}
