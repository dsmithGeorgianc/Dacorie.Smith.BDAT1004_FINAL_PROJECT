<template>
  <main>
    <div class="relative isolate overflow-hidden pt-16">


      <!-- Stats -->
      <div class="border-b border-b-gray-900/10 lg:border-t lg:border-t-gray-900/5">
        <dl class="mx-auto grid max-w-7xl grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 lg:px-2 xl:px-0">
        </dl>
      </div>

      <div
          class="absolute left-0 top-full -z-10 mt-96 origin-top-left translate-y-40 -rotate-90 transform-gpu opacity-20 blur-3xl sm:left-1/2 sm:-ml-96 sm:-mt-10 sm:translate-y-0 sm:rotate-0 sm:transform-gpu sm:opacity-50"
          aria-hidden="true">
        <div class="aspect-[1154/678] w-[72.125rem] bg-gradient-to-br from-[#FF80B5] to-[#9089FC]"
             style="clip-path: polygon(100% 38.5%, 82.6% 100%, 60.2% 37.7%, 52.4% 32.1%, 47.5% 41.8%, 45.2% 65.6%, 27.5% 23.4%, 0.1% 35.3%, 17.9% 0%, 27.7% 23.4%, 76.2% 2.5%, 74.2% 56%, 100% 38.5%)"/>
      </div>
    </div>

    <div class="mx-auto max-w-8xl px-4 sm:px-6 lg:px-8">

       <div class="text-center">
        <h1 class="text-5xl font-bold leading-tight text-gray-900">Global Stock Market Tracker</h1>
        <p class="mt-2 text-xl text-gray-600">Analyze and track the performance of major stocks in real-time</p>
      </div>


      <div class="grid grid-cols-3 gap-3">
        <div></div>
        <div>
          <div class="mx-auto max-w-md">
            <Menu as="div" class="relative inline-block text-left mt-1 p-1.5">
              <MenuButton
                  class="inline-flex w-full justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-100 focus:ring-indigo-500">
                Select Stock
                <ChevronDownIcon class="-mr-1 ml-2 h-5 w-5" aria-hidden="true"/>
              </MenuButton>
              <Transition enter-active-class="transition ease-out duration-100"
                          enter-from-class="transform opacity-0 scale-95"
                          enter-to-class="transform opacity-100 scale-100"
                          leave-active-class="transition ease-in duration-75"
                          leave-from-class="transform opacity-100 scale-100"
                          leave-to-class="transform opacity-0 scale-95">
                <MenuItems
                    class="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                  <div class="py-1">
                    <template v-for="(stock, index) in stockOptions" :key="index">
                      <MenuItem>
                        <button
                            class="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
                            @click="selectStock(stock)">{{ stock }}
                        </button>
                      </MenuItem>
                    </template>
                  </div>
                </MenuItems>
              </Transition>
            </Menu>
          </div>
        </div>
        <div></div>
      </div>

      <div>

        <dl class="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-3">
          <div v-for="item in calculatedStats" :key="item.name"
               class="overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:p-6">
            <dt class="truncate text-sm font-medium text-gray-500">{{ item.name }}</dt>
            <dd class="mt-1 text-3xl font-semibold tracking-tight text-gray-900">{{ item.value }}</dd>
          </div>
        </dl>
      </div>

      <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="p-4 border border-gray-200 rounded-lg shadow">
          <h2 v-if="selectedStockName">{{ selectedStockName }}</h2>


          <div class="p-1">
            <other-metric-charts :stockData="selectedStockData"></other-metric-charts>
          </div>


        </div>
        <div class="p-4 border border-gray-200 rounded-lg shadow">
          <div>
            <my-chart :stockData="selectedStockData"></my-chart>
          </div>
        </div>
      </div>

      <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="p-1">
          <chart-market-cap :stockData="selectedStockData"></chart-market-cap>
        </div>

        <div class="p-1">
          <chart-volume :stockData="selectedStockData"></chart-volume>
        </div>
      </div>

    </div>


  </main>
</template>

<script setup>
import {ref, computed} from 'vue';

import axios from 'axios';

import MyChart from '../components/MyChart.vue';
import OtherMetricCharts from '../components/OtherMetricCharts.vue';
import ChartMarketCap from '../components/ChartMarketCap.vue';
import ChartVolume from '../components/ChartVolume.vue';

import {Menu, MenuButton, MenuItem, MenuItems, Transition} from '@headlessui/vue';
import {ChevronDownIcon} from '@heroicons/vue/20/solid';

const stockOptions = ref(['AI', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']);
const selectedStockName = ref("")
const selectedStockData = ref([]);

const selectStock = async (stock) => {
  try {
    const response = await axios.get('http://localhost:5040/store/quotes/get_item_by_symbol/' + stock, {});
    var data = response.data.data;
    selectedStockData.value = data[0]; // Assuming the API returns an array
    //console.log("Reach")
    //console.log(response.data.data)

    selectedStockData.value = response.data.data;
    selectedStockName.value = stock
    //console.log(selectedStockData);
  } catch (error) {

    console.error(error);
  }


  /*  try {
      const response = await fetch(`http://localhost:5040/store/quotes/get_item_by_symbol/${stock}`);
      console.log(response)
      console.log("3232")
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      selectedStockData.value = data[0]; // Assuming the API returns an array
    } catch (error) {
      console.error('Error fetching stock data:', error);
      selectedStockData.value = null;
    }*/
};
const calculatedStats = computed(() => {
  if (!selectedStockData.value || selectedStockData.value.length === 0) {
    return [];
  }

  let totalChange = 0, totalDayLow = 0, totalDayHigh = 0, totalYearHigh = 0, totalYearLow = 0, totalMarketCap = 0,
      totalPriceAvg50 = 0, totalPriceAvg200 = 0, totalPrice = 0;

  selectedStockData.value.forEach(stock => {
    totalChange += stock.change;
    totalDayLow += stock.dayLow;
    totalDayHigh += stock.dayHigh;
    totalYearHigh += stock.yearHigh;
    totalYearLow += stock.yearLow;
    totalMarketCap += stock.marketCap;
    totalPriceAvg50 += stock.priceAvg50;
    totalPriceAvg200 += stock.priceAvg200;
    totalPrice += stock.price;
  });

  const avgChange = totalChange / selectedStockData.value.length;
  const avgDayLow = totalDayLow / selectedStockData.value.length;
  const avgDayHigh = totalDayHigh / selectedStockData.value.length;
  const avgYearHigh = totalYearHigh / selectedStockData.value.length;
  const avgYearLow = totalYearLow / selectedStockData.value.length;
  const avgMarketCap = totalMarketCap / selectedStockData.value.length;
  const avgPriceAvg50 = totalPriceAvg50 / selectedStockData.value.length;
  const avgPriceAvg200 = totalPriceAvg200 / selectedStockData.value.length;
  const avgPrice = totalPrice / selectedStockData.value.length;

  return [
    {name: 'Average Change', value: avgChange.toFixed(2) + ' USD'},
    {name: 'Average Day Low', value: avgDayLow.toFixed(2) + ' USD'},
    {name: 'Average Day High', value: avgDayHigh.toFixed(2) + ' USD'},
    {name: 'Average Year High', value: avgYearHigh.toFixed(2) + ' USD'},
    {name: 'Average Year Low', value: avgYearLow.toFixed(2) + ' USD'},
    {name: 'Average Market Cap', value: (avgMarketCap / 1e9).toFixed(2) + ' Billion USD'},
    {name: 'Average 50-Day Price', value: avgPriceAvg50.toFixed(2) + ' USD'},
    {name: 'Average 200-Day Price', value: avgPriceAvg200.toFixed(2) + ' USD'},
    {name: 'Average Price', value: avgPrice.toFixed(2) + ' USD'},
    // ... other stats ...
  ];
});


</script>