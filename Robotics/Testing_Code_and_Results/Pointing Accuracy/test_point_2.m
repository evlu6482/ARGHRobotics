%% House Keeping
clear all; close all; clc;

%{
    Purpose: 
        Allow user inputs for pointing accuracy tests of UR10e, takes inputs of
        goal x , y , z state and test x , y , z state.
        
        Compute Average, Maximum, and Minimum Offset in mm for pointing accuracy data

        Compute Average, Maximum, and Minimum Relative Error for pointing
        accuracy data
        
    Inputs: none
    Ouptuts: txt file including shit
  
    Project: ARGH
    Author: Connor O'Reilly
    Last Edited: 02/28/2022
%}


%% Initialization and Initial prompting 

%initialization for variables unreliant  on num_tests
avg_rel_err_x = zeros( 2 , 1 );  %for recording average relative error [outliers, no outliers]
avg_rel_err_y = zeros( 2 , 1 );
avg_rel_err_z = zeros( 2 , 1 );
avg_offset_mm_x =  zeros( 2 , 1 ); %for recording average offsets [outliers, no outliers]
avg_offset_mm_y =  zeros( 2 , 1 );
avg_offset_mm_z = zeros( 2 , 1 );
indexes = zeros( 6 , 1 ); %recording location of min and max values
max_offset_x = zeros( 2 , 1 ); %recording max values
max_offset_y = zeros( 2 , 1 );
max_offset_z = zeros( 2 , 1 );

% prompt user for test member names 
prompt = "enter name of testers in format of Member1_Member2_..._MemberN: ";
members = input(prompt, 's');

%prompt user for test date
prompt = "Enter date in format of MM_DD_YYYY: ";
dt = input(prompt, 's');

%prompt user for number of tests to run
prompt = "number of tests to run:";
num_tests = input(prompt);

%initialize size for variables relient on num_tests

test = zeros( num_tests , 3 ); %for recording values after command
goal = zeros( num_tests , 3 ); %for recording goal position values
offset = zeros( num_tests , 3 ); %for recording offset between actual and goal positions
rel_err = zeros( num_tests , 3 ); %for recording the percent error between goal values and test data

%% Un comment for loop if recording new data

%run for number of tests
% for i = 1:num_tests
%     
%         
%     fprintf('\nCurrent Test: %i\n',i)
%     disp('============================')
%     disp('Enter position of defined goal state in meters')
%         
%     %prompt and get input from user for goal x,y,z
%     prompt = 'enter goal x: ';
%     goal_x = input(prompt);
%     prompt = 'enter goal y: ';
%     goal_y = input(prompt);
%     prompt = 'enter goal z: ';
%     goal_z = input(prompt);
%     disp('============================')
% 
%         store to goal state matrix
%     goal(i,:) = [goal_x, goal_y, goal_z];
%     
%     disp('============================')
%     disp('Enter position of actual state in meters')
%     
%     %prompt and get input from user for recorded test values
%     prompt = 'enter x: ';
%     x = input(prompt);
%      prompt = 'enter y: ';
%     y = input(prompt);
%      prompt = 'enter z: ';
%     z = input(prompt);
%     disp('============================')
%     
%     %store in test value matrix
%     test(i,:) = [x,y,z];
%     
% end


%% Use lines 65-66 if importing matrix
%import matrices due to shit coding
goal = cell2mat(struct2cell(load('goal_test')));
test = cell2mat(struct2cell(load('actual_test')));

%  Also changing units from meters to mm for easier error calculation,
%  getting weird values with smaller numbers due to roundoff

%% Error Calculation

%{ 
    okay  this is going to be ugly
    conditional to check if goal state is zero, if so only multiply abs test value by 100
    conditional to check if goal state and test state have different
    signs, if so take the ratio of test abs(value)/goal * 100
    conditional to check if signs are the same, if so abs( (test-goal) /
    goal) * 100
%}
for i = 1 : num_tests
    for j = 1:3
        
        
        %first conditional check to see if goal state is equal to zero
        if(goal( i , j ) == 0)
            offset( i , j ) = test(i , j); %offset is equal to test value
            rel_err( i , j ) = abs( offset( i , j ) ) * 100; %rel error is equal to just the offset
            
        else
        %enters if goal state is non zero    
        
            %conditional to check if signs are the same, dont have to worry
            %about exact zeros due to accuracy of robotic arm and also goal
            %state zero check from prior conditional
            if( sign( test( i , j) ) == sign( goal( i , j ) ) )
                %same sign
                
                %offset is just the absolute value of the difference
                %between the test and goal
                offset( i , j ) = abs(test(i , j) - goal( i , j ) );
                
                %rel error is just the absolute offset / abs goal * 100
                
                rel_err( i , j ) = abs(  offset( i , j )  / goal( i , j ) ) * 100;
            else
                %takes care of case where both goal state and test value
                %have different sign
                
                %if test value is negative, goal is postiive, offset is
                %goal + abs(test)
                if( sign( test( i , j ) ) == -1 )
                    %test value is negaitve, goal is positive
                    offset( i , j ) = abs( test( i , j) ) + goal( i , j );
                    rel_err(i , j) = ( abs( test( i , j ) )/goal( i , j ) ) * 100;
                else
                    %test value is positive, goal is negative
                    offset( i , j ) = test( i , j ) + abs( goal( i , j ) );
                    rel_err( i , j ) = test( i , j )/abs( goal( i , j ) ) * 100;
                end
          
            end
            
        end
    
    end
end



%% regular evaluation, including possible boof values

%convert offset to mm from meters to compare to pose repeatibility
offset = offset * 100;

%compute average offset in x y and z in mm
avg_offset_mm_x(1) = mean( offset( : , 1 ) );
avg_offset_mm_y(1) = mean( offset( : , 2 ) );
avg_offset_mm_z(1) = mean( offset( : , 3 ) );

%Compute average relative error in x y and z
avg_rel_err_x(1) = mean( rel_err( : , 1 ) );
avg_rel_err_y(1) = mean( rel_err( : , 2 ) );
avg_rel_err_z(1) = mean( rel_err( : , 3 ) );

%finding max, min for above values in mm
[ min_offset_x(1) , max_offset_x(1) ] = bounds( offset( : , 1 ) );
[ min_offset_y(1) , max_offset_y(1) ] = bounds( offset( : , 2 ) );
[ min_offset_z(1) , max_offset_z(1) ] = bounds( offset( : , 3 ) );

%finding max, min for relative error 
[ min_rel_err_x(1) , max_rel_err_x(1) ] = bounds( rel_err( : , 1 ) );
[ min_rel_err_y(1) , max_rel_err_y(1) ] = bounds( rel_err( : , 2 ) );
[ min_rel_err_z(1) , max_rel_err_z(1) ] = bounds( rel_err( : , 3 ) );

%% Okay now for sketchy math

%deleting all "outliers" in data, im assuming values > 50% avg could be due
%to user error

%average offset excluding max min outliers, second index is length of
%matrix + index so subtracting height of matrix from index

%getting indexes
indexes(1:2) = find( offset( : , 1 ) == [ max_offset_x( 1 ) , min_offset_x( 1 ) ] );
indexes(3:4) = find(offset( : , 2 ) == [ min_offset_y(1) , max_offset_y(1) ] );
indexes(5:6) = find(offset( : , 3 ) == [ max_offset_z( 1 ) , min_offset_z( 1 ) ] );

%subtracting height from indexes
indexes(2:2:end) = indexes(2:2:end) - num_tests;

%get rid of repeat indexes
indexes = unique(indexes);

%reshaping offset and percent error for outliers, removes rows specified in
%indexes array. 
offset_noout = offset( setdiff( 1 : size( offset , 1 ) ,  indexes ) , : );
rel_err_noout = rel_err( setdiff( 1 : size(rel_err , 1 ), indexes ) , : );

%compute avg values, min, max for new matrixes, still in mm
avg_offset_mm_x(2) = mean( offset_noout( : , 1 ) );
avg_offset_mm_y(2) = mean( offset_noout( : , 2 ) );
avg_offset_mm_z(2) = mean( offset_noout( : , 3 ) );

%Compute average relative error in x y and z
avg_rel_err_x(2) = mean( rel_err_noout( : , 1 ) );
avg_rel_err_y(2) = mean( rel_err_noout( : , 2 ) );
avg_rel_err_z(2) = mean( rel_err_noout( : , 3 ) );

%finding max, min for above values in mm
[ min_offset_x(2) , max_offset_x(2) ] = bounds( offset_noout( : , 1 ) );
[ min_offset_y(2) , max_offset_y(2) ] = bounds( offset_noout( : , 2 ) );
[ min_offset_z(2) , max_offset_z(2) ] = bounds( offset_noout( : , 3 ) );

%finding max, min for relative error 
[ min_rel_err_x(2) , max_rel_err_x(2) ] = bounds( rel_err_noout( : , 1 ) );
[ min_rel_err_y(2) , max_rel_err_y(2) ] = bounds( rel_err_noout( : , 2 ) );
[ min_rel_err_z(2) , max_rel_err_z(2) ] = bounds( rel_err_noout( : , 3 ) );
%% File Edititing 

%create txt file and output 
filenam = strcat(members,'_', dt, '_pointing_test.txt');
fileID = fopen(filenam,'wt');
fprintf(fileID, '============================\n');
fprintf(fileID, 'Results from %i tests without removing outliers: \n', num_tests);
fprintf(fileID, '============================\n');
fprintf(fileID, ' Max offset in X position : %f [mm]\n',max_offset_x( 1 ) );
fprintf(fileID, ' Max offset in Y position : %f [mm]\n',max_offset_y( 1 ) );
fprintf(fileID, ' Max offset in Z position : %f [mm]\n',max_offset_z( 1 ) );
fprintf(fileID, '-----------------------------------------------\n');
fprintf(fileID, ' Min offset in X position : %f [mm]\n',min_offset_x( 1 ) );
fprintf(fileID, ' Min offset in Y position : %f [mm]\n',min_offset_y( 1 ) );
fprintf(fileID, ' Min offset in Z position : %f [mm]\n',min_offset_z( 1 ) );
fprintf(fileID, '-----------------------------------------------\n');
fprintf(fileID, ' Avg offset in X position : %f [mm]\n',avg_offset_mm_x( 1 ) );
fprintf(fileID, ' Avg offset in Y position : %f [mm]\n',avg_offset_mm_y( 1 ) );
fprintf(fileID, ' Avg offset in Z position : %f [mm]\n',avg_offset_mm_z( 1 ) );
fprintf(fileID, '-----------------------------------------------\n');
fprintf(fileID, ' Max Relative Error in X position : %f [%%]\n',max_rel_err_x( 1 ) );
fprintf(fileID, ' Max Relative Error in Y position : %f [%%]\n',max_rel_err_y( 1 ) );
fprintf(fileID, ' Max Relative Error in Z position : %f [%%]\n',max_rel_err_z( 1 ) );
fprintf(fileID, '-----------------------------------------------\n');
fprintf(fileID, ' Min Relative Error in X position : %f [%%]\n',min_rel_err_x( 1 ) );
fprintf(fileID, ' Min Relative Error in Y position : %f [%%]\n',min_rel_err_y( 1 ) );
fprintf(fileID, ' Min Relative Error in Z position : %f [%%]\n',min_rel_err_z( 1 ) );
fprintf(fileID, '-----------------------------------------------\n');
fprintf(fileID, ' Avg Relative Error in X position : %f [%%]\n', avg_rel_err_x( 1 ) );
fprintf(fileID, ' Avg Relative Error in Y position : %f [%%]\n', avg_rel_err_y( 1 ) );
fprintf(fileID, ' Avg Relative Error in Z position : %f [%%]\n', avg_rel_err_z( 1 ) );
fprintf(fileID, '%%%%%%%%%%%%%%%%%%%%%%%%\n');
fprintf(fileID, '%%%%%%%%%%%%%%%%%%%%%%%%\n');
fprintf(fileID, '%%%%%%%%%%%%%%%%%%%%%%%%\n');
fprintf(fileID, '============================\n');
fprintf(fileID, 'Results from %i tests with removing outliers: \n', num_tests);
fprintf(fileID, '============================\n');
fprintf(fileID, ' Max offset in X position : %f [mm]\n',max_offset_x( 2 ) );
fprintf(fileID, ' Max offset in Y position : %f [mm]\n',max_offset_y( 2 ) );
fprintf(fileID, ' Max offset in Z position : %f [mm]\n',max_offset_z( 2 ) );
fprintf(fileID, '-----------------------------------------------\n');
fprintf(fileID, ' Min offset in X position : %f [mm]\n',min_offset_x( 2 ) );
fprintf(fileID, ' Min offset in Y position : %f [mm]\n',min_offset_y( 2 ) );
fprintf(fileID, ' Min offset in Z position : %f [mm]\n',min_offset_z( 2 ) );
fprintf(fileID, '-----------------------------------------------\n');
fprintf(fileID, ' Avg offset in X position : %f [mm]\n',avg_offset_mm_x( 2 ) );
fprintf(fileID, ' Avg offset in Y position : %f [mm]\n',avg_offset_mm_y( 2 ) );
fprintf(fileID, ' Avg offset in Z position : %f [mm] \n',avg_offset_mm_z( 2 ) );
fprintf(fileID, '-----------------------------------------------\n');
fprintf(fileID, ' Max Relative Error in X position : %f [%%]\n',max_rel_err_x( 2 ) );
fprintf(fileID, ' Max Relative Error in Y position : %f [%%]\n',max_rel_err_y( 2 ) );
fprintf(fileID, ' Max Relative Error in Z position : %f [%%]\n',max_rel_err_z( 2 ) );
fprintf(fileID, '-----------------------------------------------\n');
fprintf(fileID, ' Min Relative Error in X position : %f [%%]\n',min_rel_err_x( 2 ) );
fprintf(fileID, ' Min Relative Error in Y position : %f [%%]\n',min_rel_err_y( 2 ) );
fprintf(fileID, ' Min Relative Error in Z position : %f [%%]\n',min_rel_err_z( 2 ) );
fprintf(fileID, '-----------------------------------------------\n');
fprintf(fileID, ' Avg Relative Error in X position : %f [%%]\n', avg_rel_err_x( 2 ) );
fprintf(fileID, ' Avg Relative Error in Y position : %f [%%]\n', avg_rel_err_y( 2 ) );
fprintf(fileID, ' Avg Relative Error in Z position : %f [%%]\n', avg_rel_err_z( 2 ) );
fprintf(fileID, '-----------------------------------------------\n');
fclose(fileID);