package sample;

import junit.framework.TestCase;

/**
 * Created by Johannes on 17.10.2015.
 */
public class EvaluationTest extends TestCase {

    public void testGetMaxTile() throws Exception {
        Board test1 = new Board(
                2,4,8,16,
                256,1024,2,2,
                4,4,8,16,
                0,0,2,2
                );
        assertEquals(Util.getLog2(1024), Evaluation.getMaxTile(test1.getBoard()));

        Board test2 = new Board(
                2,4,8,16,
                0,0,2,2,
                4,4,8,16,
                0,0,2,2
        );

        assertEquals(Util.getLog2(16), Evaluation.getMaxTile(test2.getBoard()));
    }

    public void testGetBoardSmoothness() throws Exception {
        Board test1 = new Board(
                2,2,0,2,
                2,2,2,2,
                4,4,4,4,
                2,2,2,2
        );


        assertEquals(-8, Evaluation.getBoardSmoothness(test1.getBoard()));

        Board test2 = new Board(
                2,2,2,2,
                2,2,2,2,
                2,2,2,2,
                2,2,2,2
        );


        assertEquals(0, Evaluation.getBoardSmoothness(test2.getBoard()));


        Board test3 = new Board(
                2,2,2,2,
                2,2,2,2,
                0,0,0,0,
                2,2,2,2
        );


        assertEquals(0, Evaluation.getBoardSmoothness(test3.getBoard()));

        Board test4 = new Board(
                0,2,2,2,
                2,0,2,0,
                0,0,0,0,
                2,0,2,2
        );


        assertEquals(0, Evaluation.getBoardSmoothness(test4.getBoard()));

        Board test5 = new Board(
                2048,1024,512,256,
                4,8,16,128,
                2,0,0,0,
                0,0,0,0
        );


        assertEquals(-31, Evaluation.getBoardSmoothness(test5.getBoard()));
    }

    public void testGetBoardMonotonicity() throws Exception {

        Board test3 = new Board(
                32,16,8,2,
                16,8,4,0,
                8,4,2,0,
                4,2,0,0
        );

        Evaluation.evaluate(test3);



    }

    public void testGetUnitMonotonicity() throws  Exception {
        Integer[] test2 = new Integer[] {128,16,8,4};
        assertEquals(0, Evaluation.getUnitMonotonicity(test2));

        Integer[] test1 = new Integer[] {4,8,16,128};
        assertEquals(-5, Evaluation.getUnitMonotonicity(test1));

        Integer[] test3 = new Integer[] {2048,1024,512,256};
        assertEquals(0, Evaluation.getUnitMonotonicity(test3));

        Integer[] test4 = new Integer[] {2048,4,2,0};
        assertEquals(0, Evaluation.getUnitMonotonicity(test4));

    }
}