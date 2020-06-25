clear all; close all; clc 

EbNo = 0:40; 
K = [4.0; 0.6]; 
M = [4; 8; 16; 64; 256]; %Positions of modulation (M-PSK or M-QAM) 

for k = 1:length(K) 
    for m = 1:length(M) 
        message = randi([0, M(m)-1], 100000, 1); 
        if M(m) >= 16 
            mod_msg = qammod(message, M(m), pi/4, 'gray'); 
            ric_ber(:, m, k) = berfading(EbNo,'qam',M(m),1,K(k)); 
        else 
            mod_msg = pskmod(message, M(m), pi/4, 'gray'); 
            ric_ber(:, m, k) = berfading(EbNo, 'psk', M(m), 1, K(k)); 
        end 
        Es = mean(abs(mod_msg).^2); 
        No = Es./((10.^(EbNo./10))*log2(M(m))); 

        h = sqrt( K(k)/(K(k)+1)) +... 
        sqrt( 1/(K(k)+1))*(1/sqrt(2))*(randn(size(mod_msg))...
         + 1j*randn(size(mod_msg))); 
        ric_msg = mod_msg.*h; % Rician flat fading 

        for c = 1:100 
            for jj = 1:length(EbNo) 
                noisy_mod = ric_msg +... 
                sqrt(No(jj)/2)*(randn(size(mod_msg))+...
                1j*randn(size(mod_msg))); %AWGN 
                noisy_mod = noisy_mod ./ h; % zero-forcing equalization 
                if M(m) >= 16 
                    demod_msg = qamdemod(noisy_mod, M(m), pi/4, 'gray'); 
                else 
                    demod_msg = pskdemod(noisy_mod, M(m), pi/4, 'gray'); 
                end 
                [number,BER(c,jj)] = biterr(message,demod_msg); 
            end 
        end 
        sum_BER(:,m, k) = sum(BER)./c; 
    end 
end 

figure(1) 

semilogy(EbNo, sum_BER(:,1,1), 'b-o', EbNo, sum_BER(:,2,1), 'r-o',... 
EbNo, sum_BER(:,3,1), 'g-o', EbNo, sum_BER(:,4,1), 'c-o',...
EbNo, sum_BER(:,5,1), 'k-o',... 
EbNo, ric_ber(:,1,1), 'b-', EbNo, ric_ber(:,2,1), 'r-',...
EbNo, ric_ber(:,3,1), 'g-', EbNo, ric_ber(:,4,1), 'c-',...
EbNo, ric_ber(:,5,1), 'k-', 'LineWidth', 1.5) 
title('Rician model (K = 4.0)') 
legend('QPSK(simulated)', '8-PSK(simulated)',... 
'16-QAM(simulated)', '64-QAM(simulated)' ,'256-QAM(simulated)',... 
'QPSK(theory)','8-PSK(theory)', '16-QAM(theory)',... 
'64-QAM(theory)' ,'256-QAM(theory)','location','best') 
xlabel('EbNo (dB)') 
ylabel('BER') 
grid on 


figure(2) 

semilogy(EbNo, sum_BER(:,1,2), 'b-o', EbNo, sum_BER(:,2,2), 'r-o',... 
EbNo, sum_BER(:,3,2), 'g-o', EbNo, sum_BER(:,4,2), 'c-o',...
EbNo, sum_BER(:,5,2), 'k-o',... 
EbNo, ric_ber(:,1,2), 'b-', EbNo, ric_ber(:,2,2), 'r-',...
EbNo, ric_ber(:,3,2), 'g-', EbNo,ric_ber(:,4,2), 'c-',...
EbNo, ric_ber(:,5,2), 'k-','LineWidth', 1.5)
title('Rician model (K = 0.6)') 
legend('QPSK(simulated)', '8-PSK(simulated)',... 
'16-QAM(simulated)', '64-QAM(simulated)' ,'256-QAM(simulated)',... 
'QPSK(theory)','8-PSK(theory)',... 
'16-QAM(theory)', '64-QAM(theory)' ,'256-QAM(theory)','location','best') 
xlabel('EbNo (dB)') 
ylabel('BER') 
grid on