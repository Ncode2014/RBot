# Using Python Slim-Buster
FROM Ncode2014/nekadok:buster

# Clone repo and prepare working directory
RUN git clone https://Ncode2014:zteam233@github.com/Ncode2014/nikabut  /home/weebproject/ \
    && chmod 777 /home/weebproject \
    && mkdir /home/weebproject/bin/

# Copies config.env (if exists)
COPY ./sample_config.env ./config.env* /home/weebproject/

# Setup Working Directory
WORKDIR /home/weebproject/

# fix aria issue
EXPOSE 80 443

# Finalization
CMD ["python3","-m","userbot"]
