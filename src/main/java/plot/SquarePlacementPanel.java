package plot;

import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseWheelEvent;
import java.awt.geom.AffineTransform;
import java.awt.geom.NoninvertibleTransformException;
import java.awt.geom.Point2D;
import java.awt.geom.Rectangle2D;
import java.util.Random;

@SuppressWarnings("serial")
public class SquarePlacementPanel extends JPanel implements Runnable {
    private AffineTransform tx = new AffineTransform();
    private final int window_size;
    private final int box_size;
    private final int wid;
    private Rectangle2D.Double[] rect;
    private Color[] color;
    private JLabel[] text;

    public SquarePlacementPanel(int id, int wsize, int bsize, Object[] X, Object[] Y, Integer[] S) {
        this.wid = id;
        this.window_size = wsize;
        this.box_size = bsize;
        this.rect = new Rectangle2D.Double[X.length];
        this.color = new Color[X.length];
        this.text = new JLabel[X.length];

        Random r = new Random();
        for (int i = 0; i < X.length; i++) {
            text[i] = new JLabel(S[i].toString(), SwingConstants.CENTER);
            rect[i] = new Rectangle2D.Double(adjust(X[i]), adjust(Y[i]), adjust(S[i]), adjust(S[i]));
            color[i] = new Color(
                    r.nextFloat() * 0.65f + 0.35f,
                    r.nextFloat() * 0.65f + 0.35f,
                    r.nextFloat() * 0.65f + 0.35f
            );
        }

        this.addMouseWheelListener(e -> {
                    double scale = 1.0;
                    Point2D p1;
                    Point2D p2 = null;

                    if (e.getScrollType() == MouseWheelEvent.WHEEL_UNIT_SCROLL) {
                        p1 = e.getPoint();
                        try {
                            p2 = tx.inverseTransform(p1, null);
                        } catch (NoninvertibleTransformException ignored) {
                        }

                        double oldscale = scale;
                        scale -= (0.2 * e.getWheelRotation());
                        scale = Math.min(Math.max(1, scale), 20);
                        if (Math.abs(oldscale - scale) < 0.1) return;

                        tx.setToIdentity();
                        tx.translate(p1.getX(), p1.getY());
                        tx.scale(scale, scale);

                        assert p2 != null;
                        tx.translate(-p2.getX(), -p2.getY());

                        SquarePlacementPanel.this.revalidate();
                        SquarePlacementPanel.this.repaint();
                    }
                }
        );
    }

    @Override
    public void paint(Graphics g) {
        super.paint(g);

        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        Shape cshape;
        Rectangle crect;
        for (int i = 0; i < rect.length; i++) {
            cshape = tx.createTransformedShape(rect[i]);
            crect = cshape.getBounds();
            g2.setColor(color[i]);
            g2.fill(cshape);
            g2.setColor(new Color(0));
            g2.draw(cshape);
            text[i].setBounds(crect);
        }
    }

    @Override
    public void run() {
        JFrame f = new JFrame("Perfect Square Placement | Instance size: " + box_size);
        f.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        for (JLabel l : text) {
            f.getContentPane().add(l);
        }
        f.getContentPane().add(this);
        f.setBounds(wid * 50, wid * 50, window_size + 7, window_size + 30);
        f.setResizable(false);
        f.setVisible(true);
    }

    private double adjust(Object num) {
        return Double.parseDouble(num.toString()) * window_size / box_size;
    }

    private double adjust(Integer num) {
        return (double) num * window_size / box_size;
    }
}
