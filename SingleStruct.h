/*
 * @Author: Wang Fei(wangfei15@cmschina.com.cn)
 * @Date: 2022-11-07 22:41:51
 * @LastEditors: Wang Fei(wangfei15@cmschina.com.cn)
 * @LastEditTime: 2022-11-07 22:42:12
 * @Description: 
 */

/**
 * @struct FundStockTransReq
 * @brief 调拨请求
 */
struct FundStockTransReq
{
    ///@brief 账号
    char fund_account[16];
    ///@brief 操作类别
    ///@ref NANO_TRANS_TYPE
    char trans_type;
    ///@brief 金额
    int correct_amt;
    ///@brief 类别
    ///@ref NANO_EXCHANGE_TYPE
    char exchange_type[4];
    ///@brief 账户
    char stock_account[16];
    ///@brief 代码
    char stock_code[12];
    ///@brief 修正数量
    int correct_vol;
};
