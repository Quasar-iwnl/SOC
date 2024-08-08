#include <iostream>
#include <vector>
#include <unordered_map>
#include "chess.hpp"
#include <cmath>
#include <memory>
#include <chrono>
#include <unordered_map>
#include <fstream>
#include <time.h>

using namespace chess;


float inf = 100000000;


// Piece values
std::unordered_map<std::string, int> PV = {
    {"pawn", 100},
    {"knight", 295},    
    {"bishop", 300},
    {"rook", 500},
    {"queen", 900},
    {"king", 1000},
    {"doubled_pawn", 80},
    {"isolated_pawn", 90},
    {"protected_pawn", 105},
    {"pawn_in_center", 110},
    {"pawn_at_7", 300},
    {"pawn_at_6", 150},
    {"pawn_promotion", 900},
    {"fianchetto", 310},
    {"bishop_in_center", 305},
    {"back_rank_bishop", 290},
    {"knight_in_center", 310},
    {"corner_knight", 285},
    {"early_queen_back_rank", 900},
    {"early_queen_else", 880},
    {"connected_rooks", 515},
    {"pig_rook", 518},
    {"pig_connected", 570},
    {"early_king_corner", 1050},
    {"late_king_center", 1100}
};

struct SortbyCond {
    bool operator()(const std::pair<int, int> &a, const std::pair<int, int> &b) {
        if (a.first != b.first) {
            return a.first < b.first;
        }
        return a.second > b.second;
    }
};

class Engine {

public:
    Board board;

    void setFen(const std::string& fen) {
        board = Board(fen);
    }
    std:: string getFen() {
        return board.getFen();
    }

    std::vector<Move> getLegalMoves() {
        std::vector<std::pair<Move, float>> pair_moves;
        std::vector<Move> legalMoves;
        Movelist moves;
        movegen::legalmoves(moves, board);
        for (const auto& move : moves) {
            std::shared_ptr<Engine> child = getChild(move);
            pair_moves.push_back({move, child->evaluate()});
        }
        std::sort(pair_moves.begin(), pair_moves.end(), [](const std::pair<Move, float>& a, const std::pair<Move, float>& b) {
            return a.second > b.second;
        });
        for (const auto& pair : pair_moves) {
            legalMoves.push_back(pair.first);
        }
        return legalMoves;
    }

    std::shared_ptr<Engine> getChild(const Move& move) {
        auto newEngine = std::make_shared<Engine>(*this);
        newEngine->makeMove(move);
        return newEngine;
    }

    void makeMove(const Move& move) {
        board.makeMove(move);
    }

    float piece_eval() { 
        float abs_eval=0;
        for(int i=0; i<64; i++) { 
            int piece = board.at(i);
            if(piece != 12) { 
                int mirrored_i = 63-i;
                if(piece < 6) { 
                    if(piece == 1) abs_eval += 3;
                    else if(piece == 2) abs_eval += 3;
                    else if(piece == 3) abs_eval += 5;
                    else if(piece == 4) abs_eval += 9;
                }
                else {
                    piece = piece-6;
                    if(piece == 1) abs_eval += 3;
                    else if(piece == 2) abs_eval += 3;
                    else if(piece == 3) abs_eval += 5;
                    else if(piece == 4) abs_eval += 9;
                }
            }
        }
        return abs_eval;
    }

    float evaluate() {

        
        const std::array<float, 64> pawns_util = {
            1000.0,    1000.0,    1000.0,    1000.0,    1000.0,    1000.0,    1000.0,    1000.0,
            150.0,   150.0,   150.0,   150.0,   150.0,   150.0,   150.0,   150.0,
            115.0,   115.0,   115.0,   125.0,   125.0,   115.0,   115.0,   115.0,
            110.0,   110.0,   110.0,   120.0,   120.0,   110.0,   110.0,    110.0,
            105.0,   105.0,   105.0,   115.0,   115.0,   105.0,   105.0,    105.0,
            101.0,   101.0,   105.0,   110.0,   110.0,   105.0,   101.0,   101.0,
            100.0,   100.0,   100.0,   100.0,   100.0,   100.0,   100.0,   100.0,
            1000.0,    1000.0,    1000.0,    1000.0,    1000.0,    1000.0,    1000.0,    1000.0,
        };
    
        const std::array<float, 64> knights_util = {
            285.0,    285.0,    285.0,    285.0,    285.0,    285.0,   285.0,    285.0,
            285.0,    305.0,   305.0,  305.0,  305.0,   305.0,   305.0,   305.0,
            285.0,   305.0,  305.0,    305.0,    305.0,   305.0,  305.0,    305.0,
            285.0,    305.0,    305.0,    306.0,   306.0,   305.0,    305.0,    285.0,
            285.0,    305.0,    305.0,   305.0,   305.0,   305.0,   305.0,    285.0,
            285.0,   300.0,   305.0,   300.0,   300.0,   305.0,   300.0,   285.0,
            285.0,   300.0,   300.0,   305.0,   305.0,   300.0,   300.0,   300.0,
            285.0,    285.0,    285.0,    285.0,    285.0,    285.0,    285.0,    285.0, 
        };
        
        const std::array<float, 64> bishops_util = {
            285.0,    285.0,    285.0,    285.0,    285.0,    285.0,    285.0,    285.0,
            300.0,    300.0,   300.0,  300.0,  300.0,   300.0,   300.0,   300.0,
            300.0,    300.0,  300.0,    300.0,    300.0,   300.0,  300.0,    300.0,
            300.0,    305.0,    300.0,    300.0,   300.0,   300.0,    303.0,    300.0,
            300.0,    300.0,    305.0,   300.0,   300.0,   305.0,   300.0,    300.0,
            300.0,    300.0,   300.0,   295.0,   295.0,   300.0,   300.0,   300.0,
            300.0,    303.0,   300.0,   301.0,   301.0,   300.0,   303.0,   300.0,
            285.0,    285.0,    285.0,    285.0,    285.0,    285.0,    285.0,    285.0,
        };
        
        const std::array<float, 64> rooks_util = {
            515.0,   515.0,  515.0,    515.0,    515.0,   515.0,  515.0,    515.0,
            515.0,    515.0,   515.0,  515.0,  515.0,   515.0,   515.0,   515.0,
            500.0,   500.0,  500.0,    500.0,    500.0,   500.0,  500.0,    500.0,
            500.0,   500.0,  500.0,    500.0,    500.0,   500.0,  500.0,    500.0,
            500.0,   500.0,  500.0,    500.0,    500.0,   500.0,  500.0,    500.0,
            500.0,   500.0,  500.0,    500.0,    500.0,   500.0,  500.0,    500.0,
            500.0,   500.0,  500.0,    500.0,    500.0,   500.0,  500.0,    500.0,
            500.0,   500.0,  500.0,    500.0,    500.0,   500.0,  500.0,    500.0,
        };
    
        const std::array<float, 64> queens_util = {
            900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0,
            900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0,
            900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0,
            900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0,
            900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0,
            900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0,
            900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0,
            900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0,
        };


        const std::array<float, 64> kings_start_util = {
            950.0,    950.0,    950.0,    950.0,    950.0,    950.0,    950.0,    950.0,
            950.0,    950.0,    950.0,    950.0,    950.0,    950.0,    950.0,    950.0,
            950.0,    950.0,    950.0,    950.0,    950.0,    950.0,    950.0,    950.0,
            950.0,    950.0,    950.0,    950.0,    950.0,    950.0,    950.0,    950.0,
            950.0,    950.0,    950.0,    950.0,    950.0,    950.0,    950.0,    950.0,
            950.0,    950.0,    950.0,    950.0,    950.0,    950.0,    950.0,    950.0,
            950.0,    950.0,    950.0,    950.0,    950.0,    950.0,    950.0,    950.0,
            960.0,    970.0,    950.0,    950.0,    950.0,    950.0,    970.0,    960.0,
        };

        const std::array<float, 64> kings_end_util = {
            700.0,    700.0,    700.0,    700.0,    700.0,    700.0,    700.0,    700.0,
            700.0,    700.0,    700.0,    700.0,    700.0,    700.0,    700.0,    700.0,
            700.0,    700.0,    700.0,    700.0,    700.0,    700.0,    700.0,    700.0,
            700.0,    700.0,    700.0,    700.0,    700.0,    700.0,    700.0,    700.0,
            700.0,    700.0,    700.0,    700.0,    700.0,    700.0,    700.0,    700.0,
            650.0,    650.0,    650.0,    650.0,    650.0,    650.0,    650.0,    650.0,
            600.0,    600.0,   600.0,   600.0,   600.0,   600.0,    600.0,    600.0,
            500.0,    500.0,   500.0,   500.0,   500.0,   500.0,    500.0,    500.0,
        };

        const std::array<float, 64> pawn_end_util = {
            1000.0,    1000.0,    1000.0,    1000.0,    1000.0,    1000.0,    1000.0,    1000.0,
            400.0,    400.0,   400.0,  400.0,  400.0,   400.0,   400.0,   400.0,
            200.0,   300.0,   300.0,   300.0,   300.0,   300.0,   300.0,   300.0,
            200.0,    200.0,    200.0,   200.0,   200.0,   200.0,   200.0,    200.0,
            170.0,    170.0,    170.0,   170.0,   170.0,   170.0,   170.0,    170.0,
            120.0,   120.0,   120.0,   120.0,   120.0,   120.0,   120.0,   120.0,
            60.0,   60.0,   60.0,   60.0,   60.0,   60.0,   60.0,   60.0,
            1000.0,    1000.0,    1000.0,    1000.0,    1000.0,    1000.0,    1000.0,    1000.0,
        };



        const std::array<const std::array<float, 64>, 8> piece_util = {pawns_util, knights_util, bishops_util, rooks_util, queens_util, kings_start_util, kings_end_util, pawn_end_util};

        float white_eval = 0, black_eval = 0;
        float pieces = piece_eval();

        

        if (board.getHalfMoveDrawType().first == GameResultReason::CHECKMATE) {
            if(board.sideToMove() == Color("w")) {
                return inf;
            } else {
                return -inf;
            }
        }
        if (board.isGameOver().second == GameResult::DRAW) {
            return 0;
        }

        for (int i=0; i<64; i++) {
            int piece = board.at(i);
            if (piece != 12) {
                int mirrored_i = 63 - i;
                if (piece < 6) { // White pieces
                    Square square(i);
                    Color defend_color = Color :: WHITE;
                    Color attack_color = Color :: BLACK;
                    Bitboard attack_board = attacks::attackers(board, attack_color, square);
                    Bitboard defend_board = attacks::attackers(board, defend_color, square);

                    float coeff = 1;
                    if(attack_board.count() > defend_board.count()) {
                        coeff = 0.35;
                    }
                    if(piece == 5) {
                        if(pieces >= 18) {
                            white_eval += coeff*piece_util[piece][mirrored_i];
                        } 
                        else {
                            white_eval += coeff*piece_util[piece+1][mirrored_i];
                        }
                    }
                    else if(piece == 0) { 
                        if(pieces  >= 18) { 
                            white_eval += coeff*piece_util[piece][mirrored_i];
                        }
                        else white_eval += coeff*piece_util[7][mirrored_i];
                    }
                    else white_eval += coeff*piece_util[piece][mirrored_i];
                     
                } 
                else { // Black pieces
                    Square square(i);
                    Color defend_color = Color :: BLACK;
                    Color attack_color = Color :: WHITE;
                    Bitboard attack_board = attacks::attackers(board, attack_color, square);
                    Bitboard defend_board = attacks::attackers(board, defend_color, square);
                    
                    float coeff = 1;
                    if(attack_board.count() > defend_board.count()) coeff = 0.35;
                    int black_piece = piece - 6;
                    if(black_piece == 5) {
                        if(pieces >= 18) {
                            black_eval += coeff*piece_util[black_piece][i];
                        } 
                        else {
                            black_eval += coeff*piece_util[black_piece+1][i];
                        }
                    }
                    else if(black_piece == 0) {
                        if(pieces >= 18) {
                            black_eval += coeff*piece_util[black_piece][i];
                        } 
                        else {
                            black_eval += coeff*piece_util[7][i];
                        }
                    }
                    else black_eval += coeff*piece_util[black_piece][i];

                }
            }
        }
        return (white_eval - black_eval);

    }


};

std::pair<float, Move> minimax(std::shared_ptr<Engine> engine, int depth, float alpha, float beta, bool maximizingPlayer) {
    if (depth == 0) { 
        return {engine->evaluate(), Move()};
    }
    else { 
        if(maximizingPlayer) {
            std::vector<Move> legalMoves = engine->getLegalMoves();
            float maxEval = -inf;
            Move bestMove;
            for (const auto& move : legalMoves) {
                std::shared_ptr<Engine> child = engine->getChild(move);
                float eval = minimax(child, depth-1, alpha, beta, false).first;
                if (eval > maxEval) {
                    maxEval = eval;
                    bestMove = move;
                }
                alpha = std::max(alpha, eval);
                if (beta <= alpha) {
                    break;
                }
            }
            return {maxEval, bestMove};
        }
        else {
            std::vector<Move> legalMoves = engine->getLegalMoves();
            float minEval = inf;
            Move bestMove;
            for (const auto& move : legalMoves) {
                std::shared_ptr<Engine> child = engine->getChild(move);
                float eval = minimax(child, depth-1, alpha, beta, true).first;
                if (eval < minEval) {
                    minEval = eval;
                    bestMove = move;
                }
                beta = std::min(beta, eval);
                if (beta <= alpha) {
                    break;
                }
            }
            return {minEval, bestMove};
        }
    }
}

std::pair<float, Move> getBetaMove(std::shared_ptr<Engine> engine, int max_time = 10000) {
        auto start = std::chrono::high_resolution_clock::now();
        int depth = 4;
        if (engine->board.sideToMove() == Color("w")) {
            float bestScore = -inf;
            Move bestMove = Move();
            float duration = 0;
            while (duration <= max_time) {
                auto start_ = std::chrono::high_resolution_clock::now();
                std::pair<float, Move> result = minimax(engine, depth, -inf, inf,  true);
                auto end = std::chrono::high_resolution_clock::now();
                float duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
                float duration_ = std::chrono::duration_cast<std::chrono::milliseconds>(end - start_).count();

                bestScore = result.first;
                bestMove = result.second;

                if (duration > max_time) {
                    break;
                }                
            }
            return {bestScore, bestMove};
        }
        float bestScore = inf;
        Move bestMove = Move();
        float duration = 0;
        while (duration <= max_time) {
            auto start_ = std::chrono::high_resolution_clock::now();
            std::pair<float, Move> result = minimax(engine, depth, -inf, inf, false);
            auto end = std::chrono::high_resolution_clock::now();
            float duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
            float duration_ = std::chrono::duration_cast<std::chrono::milliseconds>(end - start_).count();
            bestScore = result.first;
            bestMove = result.second;

            if (duration > max_time) {
                break;
            }
        }
        return {bestScore, bestMove};
    }

void sendResponse(const std::string& response) {
    std::cout << response << std::endl;
}

void handleUci() {
    sendResponse("id name ihatemyself<3");
    sendResponse("id author Quasar");
    sendResponse("uciok");
}

void handleIsReady() {
    sendResponse("readyok");
}


void handleQuit() {
    // Clean up and exit
    exit(0);
}

int main() {
    std::string command;
    Engine engine = Engine();
    while (std::getline(std::cin, command)) {
        if (command == "uci") {
            handleUci();
        } else if (command == "isready") {
            handleIsReady();
        } else if (command.substr(0, 8) == "position") {
            std::istringstream iss(command);
            std::string token;
            iss >> token; // "position"

            std::string positionType;
            iss >> positionType;

            if (positionType == "startpos") {
                // Set up initial position
                // engine = Engine();
                engine.board = Board();
                iss >> token; // Check if there are more tokens, should be "moves" or end of string
            } else if (positionType == "fen") {
                // Read FEN string
                std::string fen;
                while (iss >> token && token != "moves") {
                    fen += token + " ";
                }
                engine.setFen(fen);
            }
            if (token == "moves") {
                std::string move;
                while (iss >> move) {
                    engine.board.makeMove(uci::uciToMove(engine.board, move));
                }
            }
        } else if(command.substr(0, 11) == "go movetime"){
            std::istringstream iss(command);
            std::string goCommand, movetimeKeyword;
            int maxTimeInMillis = 10000;
            iss >> goCommand >> movetimeKeyword >> maxTimeInMillis;
            std::cout << "Max time per move: " << maxTimeInMillis << std::endl;
            auto move = getBetaMove(std::make_shared<Engine>(engine), maxTimeInMillis);
            std::string string_move = uci::moveToUci(move.second);
            sendResponse("bestmove " + string_move);
        } else if(command.substr(0, 2) == "go") {
            auto move = getBetaMove(std::make_shared<Engine>(engine), 10000);
            // std::cout<<"Didnt Reach here";
            std::string string_move = uci::moveToUci(move.second);
            sendResponse("bestmove " + string_move);
        } else if (command == "quit") {
            handleQuit();
        }
    }
    return 0;
}