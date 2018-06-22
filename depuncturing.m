%Fuction for depuncturing
%by Vladimir Fadeev
%vladimir_fadeev1993@mail.ru

% inputs:
%         punctured - punctured vector
%         punct_vec - puncturing vector
%         shouldbe - length of message before puncturing

% output:
%         depunctured - reconstructed vector


function depunctured = depuncturing(punctured,punct_vec,shouldbe)

%Calculation how much ones we have in puncturing vector:
counter = 0;
for i = 1:length(punct_vec)
    if punct_vec(i) == 1
        counter = counter + 1;
    end
end


%Depuncturing
depunctured = zeros(shouldbe,1); %+ 12),1);
shift = 0;
shift2 = 0;
len2 = length(punct_vec);
for i = 1:length(depunctured)
    if punct_vec(i - shift2*len2) == 0
       shift = shift + 1;
       depunctured(i) = 0;
    else depunctured(i) = punctured(i-shift);
    end
    if mod(i,len2) == 0
       shift2 = shift2 + 1;
    end
end
end