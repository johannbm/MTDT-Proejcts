package sample;

import org.apache.commons.lang3.tuple.Pair;

/**
 * Created by Johannes on 10.10.2015.
 */
public class Tile extends Pair {

    private int x;
    private int y;

    public Tile(int x, int y) {
        this.x = x;
        this.y = y;
    }

    @Override
    public Object getLeft() {
        return x;
    }

    @Override
    public Object getRight() {
        return y;
    }

    @Override
    public int compareTo(Object o) {
        return 0;
    }

    @Override
    public Object setValue(Object value) {
        return null;
    }
}
