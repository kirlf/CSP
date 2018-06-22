%Fuction for puncturing
%by Vladimir Fadeev
%vladimir_fadeev1993@mail.ru

% inputs:
%         punctured - message vector
%         punct_vec - puncturing vector

% output:
%         punctured - punctured vector

function punctured = puncturing(message,punct_vec)
counter = 0;
for i = 1:length(punct_vec)
    if punct_vec(i) == 1
        counter = counter +1;
    end
end


shift = 0;
shift2 = 0;
len2 = length(punct_vec);
for j = 1:length(message) 
    if punct_vec(j-shift2*len2) == 1
       punctured(j - shift) =  message(j);
    else shift = shift + 1;

    end
    if mod(j,len2) == 0
    shift2 = shift2 +1;
    end
end
end