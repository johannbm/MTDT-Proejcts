package sample;

/**
 * Created by Johannes on 14.10.2015.
 */
public class AI {

    public static Board resultBoard;
    private static final float MIN_ALPHA = -100000;
    private static final float MAX_BETA = 100000;


    public static Direction alphaBetaPruning(Board state, int depth, int maxDepth, float a, float b, boolean maxPlayer) {
        resultBoard = null;

        float maxValue = alphaBetaSearch2(state, depth, maxDepth, a, b, maxPlayer);

        return resultBoard.findBoardPath();
    }

    public static float alphaBetaSearch2(Board state, int depth, int maxDepth, float a, float b, boolean maxPlayer) {
        if (depth == 0 || state.isGameOver()) {
            return Evaluation.evaluate(state);
        }

        if (maxPlayer) {
            float value = MIN_ALPHA;
            for (Board board : Util.getNextPossibleBoards(state).values()) {
                value = Math.max(value, alphaBetaSearch2(board, depth-1, maxDepth, a, b, false));

                if (depth == maxDepth) {
                    if (value > a) {
                        resultBoard = board;
                    }
                }

                a = Math.max(a, value);
                if (b <= a)
                    break;
            }
            return value;
        }
        else {
            float value = MAX_BETA;
            for (Board board : Util.getNextPossibleRandomBoards(state)) {
                value = Math.min(value, alphaBetaSearch2(board, depth, maxDepth, a, b, true));
                b = Math.min(b, value);
                if (b <= a)
                    break;
            }

            return value;
        }
    }

}
