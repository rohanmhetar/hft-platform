#include <boost/asio.hpp>
#include <thread>
#include <iostream>
#include <queue>
#include <mutex>
#include <condition_variable>
#include <string>

class OrderExecutor {
public:
    OrderExecutor() 
        : io_service_(), work_(io_service_), executor_thread_([this]() { io_service_.run(); }) {
        std::cout << "OrderExecutor initialized." << std::endl;
    }

    ~OrderExecutor() {
        io_service_.stop();
        if (executor_thread_.joinable()) {
            executor_thread_.join();
        }
        std::cout << "OrderExecutor terminated." << std::endl;
    }

    void execute_order(const std::string& order) {
        boost::asio::post(io_service_, [order]() {
            // Simulate order execution latency
            std::this_thread::sleep_for(std::chrono::milliseconds(10));
            std::cout << "Executed order: " << order << std::endl;
        });
    }

    void execute_bulk_orders(const std::vector<std::string>& orders) {
        for (const auto& order : orders) {
            execute_order(order);
        }
    }

private:
    boost::asio::io_service io_service_;
    boost::asio::io_service::work work_;
    std::thread executor_thread_;
};

extern "C" {
    OrderExecutor* OrderExecutor_new() { return new OrderExecutor(); }
    void OrderExecutor_execute(OrderExecutor* executor, const char* order) { executor->execute_order(std::string(order)); }
    void OrderExecutor_execute_bulk(OrderExecutor* executor, const char** orders, int count) {
        std::vector<std::string> bulk_orders;
        for(int i = 0; i < count; ++i) {
            bulk_orders.emplace_back(std::string(orders[i]));
        }
        executor->execute_bulk_orders(bulk_orders);
    }
    void OrderExecutor_delete(OrderExecutor* executor) { delete executor; }
}
