import java.util.Vector;

public class strategy_swerve_bezier_1 {
    final double p1X, p1Y;
    final double p2X, p2Y;
    final double p3X, p3Y;
    final double p4X, p4Y;
    final double tScale;

    public strategy_swerve_bezier_1(double p1X, double p1Y, double p2X, double p2Y, double p3X, double p3Y, double p4X, double p4Y, double tScale) {
        this.p1X = p1X;
        this.p1Y = p1Y;
        this.p2X = p2X;
        this.p2Y = p2Y;
        this.p3X = p3X;
        this.p3Y = p3Y;
        this.p4X = p4X;
        this.p4Y = p4Y;
        this.tScale = 1.0 / tScale;
    }

    // calculations from current pos to target pos
    private Vertex homePoint(Vertex target, Vertex curr, double maxSpeed) {
        double x = Math.max(Math.min(target.x - curr.x, maxSpeed), -maxSpeed);
        double y = Math.max(Math.min(target.y - curr.y, maxSpeed), -maxSpeed);
        return Vertex.fromCart(x, y);
    }

    private Vertex bezierTag(double time) {
        double t = Math.max(Math.min(time * tScale, 1.0), 0.0);
        double x = calc_bezier(p1X, p2X, p3X, p4X, t);
        double y = calc_bezier(p1Y, p2Y, p3Y, p4Y, t);
        return Vertex.fromCart(x, y);
    }

    // bezier curve calculation
    private double calc_bezier(double p1, double p2, double p3, double p4, double t) {
        return Math.pow(1.0 - t, 3) * p1
                + 3.0 * t * Math.pow(1.0 - t, 2) * p2
                + 3.0 * Math.pow(t, 2) * (1.0 - t) * p3
                + Math.pow(t, 3) * p4;
    }

    // main pathfinding strategy
    public static void main(String[] args) {
        double p1X = 2, p1Y = -12; //current pos
        double p2X = 9, p2Y = -10; //p2
        double p3X = 3, p3Y = -3; //p3
        double p4X = 2, p4Y = -1; //target location
        double tScale = 175.0;

        strategy_swerve_bezier_1 bezierStrategy = new strategy_swerve_bezier_1(p1X, p1Y, p2X, p2Y, p3X, p3Y, p4X, p4Y, tScale);

        double time = 50;
        Vertex target = bezierStrategy.bezierTag(time);

        // current location
        Vertex curr = Vertex.fromCart(2, -12);
        double maxSpeed = 1.0;

        // calculations for next home point
        Vertex nextPoint = bezierStrategy.homePoint(target, curr, maxSpeed);
    }
}

// vertex thingie
class Vertex {
    public final double x, y;

    private Vertex(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public static Vertex fromCart(double x, double y) {
        return new Vertex(x, y);
    }

    @Override
    public String toString() {
        return "Vertex{" + "x=" + x + ", y=" + y + '}';
    }
}
