from solution import Solution


############### GROUP 1 ##############

# Question 1
solution_g1_q1 = Solution(file_path=".\solution\g1-q1.py", question_number="1", group_number='1', run_from_main=True)
solution_g1_q1.inputs_to_test = ["VinUni is a young institution\nand elite\n", 
                                "Hi my name is Jack\nthe reaper\n",
                                "I really really like pancakes\nwith bacon\n"]

# Question 2
solution_g1_q2 = Solution(file_path=".\solution\g1-q2.py", question_number="2", group_number='1', run_from_main=True)
solution_g1_q2.inputs_to_test = ["5\n20\n80\n100\n90\n50\n",
                                "95\n2\n4\n"]

# Question 3a
solution_g1_q3a = Solution(file_path=".\solution\g1-q3a.py", question_number="3a", group_number='1', run_from_main=False)
solution_g1_q3a.inputs_to_test = [[1,3,4,5],
                                [-2,0,2,4,6,8],
                                [1,-3,3,7]]
solution_g1_q3a.functions_to_test = "odds_sum"

# Question 3b
solution_g1_q3b = Solution(file_path=".\solution\g1-q3b.py", question_number="3b", group_number='1', run_from_main=False)
solution_g1_q3b.inputs_to_test = [4, 8, -27, 0, 27, 1331, -1331]
solution_g1_q3b.functions_to_test = "cube_root"

# Question 4
solution_g1_q4 = Solution(file_path=".\solution\g1-q4.py", question_number="4", group_number='1', run_from_main=False, multi_input=True)
solution_g1_q4.functions_to_test = "add_matrix"
solution_g1_q4.inputs_to_test = [[[[1,2,3], [1,5,1], [1,2,2]], [[3,1,0], [1,1,2], [2,1,0]]],
                            [[[4, 3, 3], [2, 6, 3], [3, 3, 2]], [[1,2,3], [1,5,1], [1,2,2]]],
                            [[[1,2],[2,3],[3,4]], [[5,6],[7,8],[9,10]]]]


############### GROUP 2 ##############


solution_dict = {
    ('1','1') : solution_g1_q1,
    ('2','1') : solution_g1_q2,
    ('3a','1'): solution_g1_q3a,
    ('3b','1'): solution_g1_q3b,
    ('4','1') : solution_g1_q4
}