package sample;

import javax.swing.plaf.DesktopIconUI;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Dictionary;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Random;

/**
 * Created by Johannes on 14.10.2015.
 */
public class Util {


    public static ArrayList<Tile> getEmptySlots(Integer[][] b) {
        ArrayList<Tile> emptySlots = new ArrayList<>();
        for (int x = 0; x < b.length; x++) {
            for (int y = 0; y < b.length; y++) {
                if (b[x][y] == 0)
                    emptySlots.add(new Tile(x, y));
            }
        }

        return emptySlots;
    }

    /**
     *
     * @param a board a
     * @param b board b
     * @return  true if boards are different
     */
    public static boolean compareBoards(Integer[][] a, Integer[][] b) {
        if (a == null) {
            return true;
        }
        for (int x = 0; x < b.length; x++) {
            for (int y = 0; y < b.length; y++) {
                if (!Objects.equals(b[x][y], a[x][y])) {
                    return true;
                }
            }
        }
        return false;
    }

    public static Integer[][] transposeBoard(Integer[][] b) {
        Integer[][] newBoard = new Integer[4][4];
        for (int x = 0; x < newBoard.length; x++) {
            for (int y = 0; y < newBoard.length; y++) {
                newBoard[y][x] = b[x][y];
            }
        }
        return newBoard;
    }

    public static Integer[] mergeTiles(Direction direction, Integer[] unit) {
        unit = filterList(unit);
        if (unit.length > 1) {
            if (direction == Direction.LEFT || direction == Direction.UP) {
                for (int i = 1; i < unit.length; i++) {
                    if (Objects.equals(unit[i - 1], unit[i])) {
                        int oldValue = unit[i];
                        unit[i - 1] = oldValue * 2;
                        unit[i] = 0;
                    }
                }
            }
            else if (direction == Direction.RIGHT || direction == Direction.DOWN) {
                for (int i = unit.length - 2; i >= 0; i--) {
                    if (Objects.equals(unit[i + 1], unit[i])) {
                        int oldValue = unit[i];
                        unit[i + 1] = oldValue * 2;
                        unit[i] = 0;
                    }
                }
            }
        }
        boolean reverse = (direction == Direction.UP || direction == Direction.LEFT);
        return restoreList(filterList(unit), !reverse);
    }

    public static Integer[] filterList(Integer[] unit) {
        ArrayList<Integer> newUnit = new ArrayList<>(Arrays.asList(unit));
        newUnit.removeAll((Collections.singletonList(0)));
        return newUnit.toArray(new Integer[newUnit.size()]);
    }

    public static Integer[] restoreList(Integer[] unit, boolean reverse) {
        Integer[] newUnit = new Integer[] {0,0,0,0};
        if (reverse) {
            int length = newUnit.length - unit.length;
            for (int i = 0; i < unit.length; i++) {
                newUnit[length + i] = unit[i];
            }
        } else {
            System.arraycopy(unit, 0, newUnit, 0, unit.length);
        }
        return newUnit;
    }

    public static Map<Direction, Board> getNextPossibleBoards(Board state) {
        Map<Direction, Board> possibleBoards = new HashMap<>();

        for (Direction dir : Direction.values()) {
            Board newState = state.getCopy();
            newState.move(dir);
            if (compareBoards(newState.getBoard(), state.getBoard())) {
                newState.move = dir;
                newState.cameFromBoard = state;
                possibleBoards.put(dir, newState);
            }
        }

        return possibleBoards;
    }

    public static ArrayList<Board> getNextPossibleRandomBoards(Board state) {
        ArrayList<Board> nextStates = new ArrayList<>();

        Random r = new Random();

        for (Tile tile : getEmptySlots(state.getBoard())) {
            Board copy1 = state.getCopy();
            copy1.cameFromBoard = state;
//            int value = (r.nextInt(100) >= 90) ? 4 : 2;
            copy1.placeTile(tile, 2);
            nextStates.add(copy1);

            Board copy2 = state.getCopy();
            copy2.cameFromBoard = state;
            copy2.placeTile(tile, 4);
            nextStates.add(copy2);
        }

        return nextStates;
    }


    public static int getLog2(int a) {
        if (a == 0)
            return 0;
        return (int)(Math.log(a) / Math.log(2));
    }

}
