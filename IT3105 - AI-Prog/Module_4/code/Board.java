package sample;

import java.util.*;

/**
 * Created by Johannes on 12.10.2015.
 */
public class Board {

    private Integer[][] board;
    public Board cameFromBoard;
    public Direction move;


    public Board() {
        board = new Integer[4][4];
        for (int x = 0; x < 4; x++) {
            for (int y = 0; y < 4; y++) {
                board[x][y] = 0;
            }
        }
    }

    public Board(int x1, int x2, int x3, int x4,
                 int x5, int x6, int x7, int x8,
                 int x9, int x10, int x11, int x12,
                 int x13, int x14, int x15, int x16) {

        board = new Integer[][] {
                new Integer[] {x1,x5,x9,x13},
                new Integer[] {x2,x6,x10,x14},
                new Integer[] {x3,x7,x11,x15},
                new Integer[] {x4,x8,x12,x16}
        };
    }

    public Integer[][] getBoard() {
        return board;
    }

    public void setBoard(Integer[][] b) {
        this.board = b;
    }

    public void move(Direction dir) {
        if (dir == Direction.UP || dir == Direction.DOWN)
            moveVertically(dir);
        else if (dir == Direction.LEFT || dir == Direction.RIGHT)
            moveHorizontally(dir);

    }

    public void moveVertically(Direction dir) {
        for (int x = 0; x < board.length; x++) {
            board[x] = Util.mergeTiles(dir, board[x]);
        }
    }

    public void moveHorizontally(Direction dir) {
        Integer[][] transposedBoard = Util.transposeBoard(board);
        for (int x = 0; x < transposedBoard.length; x++) {
            transposedBoard[x] = Util.mergeTiles(dir, transposedBoard[x]);

        }
        board = Util.transposeBoard(transposedBoard);
    }

    public boolean isGameOver() {
        boolean canMerge = false;

        //Checking horizontally
        for (Integer[] row : board) {
            for (int i = 1; i < row.length; i++) {
                if (Objects.equals(row[i - 1], row[i])) {
                    canMerge = true;
                }
            }
        }

        for (Integer[] row : Util.transposeBoard(board)) {
            for (int i = 1; i < row.length; i++) {
                if (Objects.equals(row[i - 1], row[i])) {
                    canMerge = true;
                }
            }
        }

        return (!canMerge && !(Util.getEmptySlots(board).size() > 0));
    }



    public void spawnTile() {
        ArrayList<Tile> emptySlots = Util.getEmptySlots(board);
        if (emptySlots.size() > 0) {
            Random r = new Random();
            Tile chosenTile = emptySlots.get(r.nextInt(emptySlots.size()));
            int percentage = r.nextInt(100);
            int chosenNumber = (percentage >= 90) ? 4 : 2;


            board[((int) chosenTile.getLeft())][(int) chosenTile.getRight()] = chosenNumber;
        }
    }

    public void printBoard() {
        for (int x = 0; x < board.length; x++) {
            System.out.println(board[0][x] + "     " + board[1][x] + "     " + board[2][x] + "     " + board[3][x]);
        }
        System.out.println("SMOOTHNESS: " + Evaluation.getBoardSmoothness(board));
        System.out.println("MONOTONICITY: " + Evaluation.getBoardMonotonicity(board));
        System.out.println("EVALUATION: " + Evaluation.evaluate(this));
        System.out.println("GAME OVER? " + isGameOver());
        System.out.println("-------------");
    }


    public Board getCopy() {
        Board b = new Board();
        Integer[][] newBoard = new Integer[4][4];
        for (int i = 0; i < 4; i++) {
            System.arraycopy(board[i], 0, newBoard[i], 0, newBoard.length);
        }
        b.setBoard(newBoard);
        return b;
    }

    public void placeTile(Tile tile, int value) {
        board[(int) tile.getLeft()][(int) tile.getRight()] = value;
    }

    public Direction findBoardPath() {
        ArrayList<Board> boardArrayList = new ArrayList<>();
        Board b = this;
        while (true) {
            boardArrayList.add(b);
        //  //b.printBoard();
            if (b.cameFromBoard != null) {
                if (b.cameFromBoard.cameFromBoard != null)
                    b = b.cameFromBoard;
                else
                    break;
            }
            else
                break;
        }
        return b.move;
        //return boardArrayList.get(boardArrayList.size()-1).move;
    }


}
