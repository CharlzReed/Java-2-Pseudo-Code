    private Boolean checkValid(int row, int col, int num) {
        Boolean valid = true;

        for (int x = 0; x < 9; x++) {
            if (board[x][col] == num) {
                valid = false;
            }
        }
        
        for (int y = 0; y < 9; y++) {
            if (board[row][y] == num) {
                valid = false;
            }
        }
        
        int rowsection = (int) row / 3;
        int colsection = (int) col / 3;
        
        for (int x = 0; x < 3; x++) {
            for (int y = 0; y < 3; y++) {
                if (board[rowsection * 3 + x][colsection * 3 + y] == num) {
                    valid = false;
                }
            }
        }
        return valid;
    }