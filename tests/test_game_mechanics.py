from CheckersTournament.game import GameMechanics
from CheckersTournament.game_elements.board import Board, Square, Vector, Move
from CheckersTournament.game_elements.piece import PieceType, PlayerId


def setup_board():
    board = Board(empty=True)
    sqr = Square(1, 1)
    fwd_vector = Vector(1, 1)
    bwd_vector = Vector(-1, -1)
    board.set_location(sqr, PieceType.man, PlayerId.white.value)
    return board, bwd_vector, fwd_vector, sqr


def test_movement_direction():
    board, bwd_vector, fwd_vector, sqr = setup_board()
    assert GameMechanics.validate_movement_vector(board, sqr, fwd_vector)
    assert not GameMechanics.validate_movement_vector(board, sqr, bwd_vector)
    board.rotate()
    assert not GameMechanics.validate_movement_vector(board, sqr, fwd_vector)
    assert GameMechanics.validate_movement_vector(board, sqr, bwd_vector)
    # Test king movement
    board.set_location(sqr, PieceType.king, PlayerId.white.value)
    assert GameMechanics.validate_movement_vector(board, sqr, fwd_vector)
    assert GameMechanics.validate_movement_vector(board, sqr, bwd_vector)
    board.rotate()
    assert GameMechanics.validate_movement_vector(board, sqr, fwd_vector)
    assert GameMechanics.validate_movement_vector(board, sqr, bwd_vector)


def test_step_in_vector():
    board, bwd_vector, fwd_vector, sqr = setup_board()
    fwd_move = Move(sqr, sqr+fwd_vector)
    bwd_move = Move(sqr, sqr+bwd_vector)
    assert not GameMechanics.check_step_in_vector(board, sqr, bwd_vector)
    assert GameMechanics.check_step_in_vector(board, sqr, fwd_vector)
    board.rotate()
    assert GameMechanics.check_step_in_vector(board, sqr, bwd_vector)
    assert not GameMechanics.check_step_in_vector(board, sqr, fwd_vector)
    board.rotate()
    # Test king
    board.set_location(sqr, PieceType.king, PlayerId.white.value)
    assert GameMechanics.check_step_in_vector(board, sqr, bwd_vector)
    assert GameMechanics.check_step_in_vector(board, sqr, fwd_vector)
    board.set_location(sqr+fwd_vector, PieceType.man, PlayerId.white.value)
    assert not GameMechanics.check_step_in_vector(board, sqr, fwd_vector)


def test_capture_in_vector():
    board, bwd_vector, fwd_vector, sqr = setup_board()
    fwd_move = Move(sqr, sqr + fwd_vector)
    fwd_move2 = Move(sqr + fwd_vector, sqr + fwd_vector + fwd_vector)
    assert GameMechanics.get_valid_captures_in_vector(board, sqr, fwd_vector) == []
    assert GameMechanics.get_valid_captures_in_vector(board, sqr, bwd_vector) == []
    sqr2 = Square(2, 2)
    board.set_location(sqr2, PieceType.man, PlayerId.white.value)
    assert GameMechanics.get_valid_captures_in_vector(board, sqr, fwd_vector) == []
    board.set_location(sqr2, PieceType.man, PlayerId.black.value)
    assert GameMechanics.get_valid_captures_in_vector(board, sqr, fwd_vector) == [fwd_move, fwd_move2]
    # Black capture backwards after rotation
    board.rotate()
    bwd_move = Move(sqr2, sqr2 + bwd_vector)
    bwd_move2 = Move(sqr2 + bwd_vector, sqr2 + bwd_vector + bwd_vector)
    assert GameMechanics.get_valid_captures_in_vector(board, sqr2, bwd_vector) == [bwd_move, bwd_move2]
    # King capture backwards after rotation
    board.set_location(sqr, PieceType.king, PlayerId.white.value)
    assert GameMechanics.get_valid_captures_in_vector(board, sqr, fwd_vector) == [fwd_move, fwd_move2]


def test_double_capture():
    board, bwd_vector, fwd_vector, sqr = setup_board()
    sqr2 = Square(2, 2)
    sqr3 = Square(3, 3)
    sqr4 = Square(4, 4)
    sqr5 = Square(5, 5)
    board.set_location(sqr2, PieceType.man, PlayerId.black.value)
    board.set_location(sqr4, PieceType.man, PlayerId.black.value)
    fwd_move = Move(sqr, sqr2)
    fwd_move2 = Move(sqr2, sqr3)
    fwd_move3 = Move(sqr3, sqr4)
    fwd_move4 = Move(sqr4, sqr5)
    assert GameMechanics.get_valid_captures(board, sqr, fwd_vector) == \
        [[fwd_move, fwd_move2, fwd_move3, fwd_move4]]
    sqr4 = Square(2, 4)
    sqr5 = Square(1, 5)
    fwd_move32 = Move(sqr3, sqr4)
    fwd_move42 = Move(sqr4, sqr5)
    board.set_location(sqr4, PieceType.man, PlayerId.black.value)
    assert sorted(GameMechanics.get_valid_captures(board, sqr, fwd_vector)) == \
        sorted([[fwd_move, fwd_move2, fwd_move3, fwd_move4],
                [fwd_move, fwd_move2, fwd_move32, fwd_move42]])


def test_crowning():
    board_str = """---------------------------------
|   |@@@|   |@@@|   |@@@|   |@@@|
---------------------------------
|@@@|   |@@@|1,0|@@@|   |@@@|2,0|
---------------------------------
|   |@@@|   |@@@|   |@@@|1,0|@@@|
---------------------------------
|@@@|   |@@@|1,0|@@@|   |@@@|   |
---------------------------------
|2,0|@@@|   |@@@|1,1|@@@|   |@@@|
---------------------------------
|@@@|   |@@@|1,1|@@@|   |@@@|   |
---------------------------------
|   |@@@|1,1|@@@|   |@@@|   |@@@|
---------------------------------
|@@@|   |@@@|   |@@@|   |@@@|   |
---------------------------------"""
    board = Board.load_from_str(board_str)
    sqr = Square(4, 4)
    moves = GameMechanics.get_valid_captures(board, sqr, True)
    board.run_moves(moves[0])
    piece, player = board.get_location(Square(0,4))
    assert piece == PieceType.king


